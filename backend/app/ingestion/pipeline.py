import traceback
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.models.job import Job, IngestionRun, IngestionError
from app.schemas.job import NormalizedJobCreate
from app.ingestion.base import JobSource
from app.ingestion.rss_source import RSSJobSource
from app.ingestion.api_source import APIJobSource
from app.ingestion.mock_source import MockJobSource
from app.ingestion.normalizer import DataNormalizer
from app.ingestion.validator import RecordValidator
from app.ingestion.deduplicator import Deduplicator
from app.config import settings
from app.utils.logger import logger

class IngestionPipeline:
    """
    Core orchestrator executing the standardized ETL pipeline:
    FETCH -> NORMALIZE -> VALIDATE -> DEDUPLICATE -> STORE -> LOG RESULT.
    Includes automated fallback handling and execution auditing.
    """

    def __init__(self, db: Session, primary_source: Optional[JobSource] = None, fallback_source: Optional[JobSource] = None):
        self.db = db
        self.primary_source = primary_source or self._resolve_source(settings.PRIMARY_SOURCE_TYPE, settings.PRIMARY_SOURCE_URL)
        self.fallback_source = fallback_source or self._resolve_source(settings.FALLBACK_SOURCE_TYPE, settings.FALLBACK_SOURCE_URL)

    def _resolve_source(self, source_type: str, source_url: str) -> JobSource:
        st = (source_type or "rss").lower()
        if st == "rss":
            return RSSJobSource(url=source_url or "https://weworkremotely.com/remote-jobs.rss")
        elif st == "api":
            return APIJobSource(url=source_url or "https://arbeitnow.com/api/job-board-api")
        elif st == "mock":
            return MockJobSource(mode="standard")
        elif st == "mock_duplicates":
            return MockJobSource(mode="with_duplicates")
        elif st == "mock_malformed":
            return MockJobSource(mode="with_malformed")
        elif st == "mock_failure":
            return MockJobSource(mode="failure")
        return RSSJobSource()

    def run(self) -> IngestionRun:
        run_record = IngestionRun(
            source=self.primary_source.source_name,
            started_at=datetime.utcnow(),
            status="running"
        )
        self.db.add(run_record)
        self.db.commit()
        self.db.refresh(run_record)

        logger.info(f"=== Starting Ingestion Run ID: {run_record.id} [Source: {run_record.source}] ===")

        raw_records = []
        active_source_name = self.primary_source.source_name
        
        # STAGE 1: FETCH (with fallback)
        try:
            raw_records = self.primary_source.fetch_jobs()
        except Exception as exc:
            primary_err = str(exc)
            logger.error(f"Primary source '{self.primary_source.source_name}' failed: {primary_err}")
            logger.info("Attempting fallback source activation...")
            
            try:
                if self.fallback_source:
                    raw_records = self.fallback_source.fetch_jobs()
                    active_source_name = f"{self.fallback_source.source_name} (Fallback)"
                    logger.info(f"Fallback source '{self.fallback_source.source_name}' succeeded.")
                else:
                    raise Exception("No fallback source configured.")
            except Exception as fallback_exc:
                error_msg = f"Primary failed ({primary_err}); Fallback failed ({str(fallback_exc)})"
                logger.critical(f"All ingestion sources failed: {error_msg}")
                
                run_record.status = "failed"
                run_record.completed_at = datetime.utcnow()
                run_record.error_message = error_msg
                self.db.commit()
                return run_record

        run_record.records_fetched = len(raw_records)
        run_record.source = active_source_name

        if not raw_records:
            logger.warning("Fetch returned 0 raw job records.")
            run_record.status = "success"
            run_record.completed_at = datetime.utcnow()
            self.db.commit()
            return run_record

        # STAGE 2 & 3: NORMALIZE & VALIDATE
        valid_records = []
        failed_count = 0

        for raw_item in raw_records:
            normalized_dict = DataNormalizer.normalize_record(raw_item, default_source=active_source_name)
            validated_record, val_error = RecordValidator.validate(normalized_dict)

            if validated_record:
                valid_records.append(validated_record)
            else:
                failed_count += 1
                ingestion_err = IngestionError(
                    run_id=run_record.id,
                    raw_record=str(raw_item)[:1000],
                    error_reason=val_error or "Validation failed"
                )
                self.db.add(ingestion_err)

        run_record.records_failed = failed_count

        # STAGE 4: DEDUPLICATE
        unique_records, skipped_duplicates = Deduplicator.filter_batch(valid_records, self.db)
        run_record.records_skipped = skipped_duplicates

        # STAGE 5: STORE DB
        inserted_count = 0
        try:
            for item in unique_records:
                job_db = Job(
                    external_id=item.external_id,
                    title=item.title,
                    company=item.company,
                    location=item.location,
                    description=item.description,
                    employment_type=item.employment_type,
                    salary=item.salary,
                    source=item.source,
                    source_url=item.source_url,
                    posted_at=item.posted_at,
                    collected_at=item.collected_at,
                    skills=item.skills,
                    remote=item.remote,
                    status=item.status,
                    content_hash=item.content_hash
                )
                self.db.add(job_db)
                inserted_count += 1
            
            self.db.commit()
            run_record.records_inserted = inserted_count
            run_record.status = "partial_success" if failed_count > 0 else "success"

        except Exception as db_exc:
            self.db.rollback()
            err_str = f"Database commit failed: {str(db_exc)}"
            logger.error(err_str)
            run_record.status = "failed"
            run_record.error_message = err_str

        run_record.completed_at = datetime.utcnow()
        self.db.commit()

        logger.info(
            f"=== Ingestion Run Completed: {run_record.status.upper()} | "
            f"Fetched: {run_record.records_fetched} | Inserted: {run_record.records_inserted} | "
            f"Skipped (Dupes): {run_record.records_skipped} | Failed: {run_record.records_failed} ==="
        )
        return run_record
