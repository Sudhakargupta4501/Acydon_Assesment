from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.job import Job, IngestionRun
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.rss_source import RSSJobSource
from app.ingestion.api_source import APIJobSource
from app.ingestion.mock_source import MockJobSource

class IngestionService:
    @staticmethod
    def trigger_run(db: Session, source_type: Optional[str] = None, source_url: Optional[str] = None) -> IngestionRun:
        primary_source = None
        if source_type:
            st = source_type.lower()
            if st == "rss":
                primary_source = RSSJobSource(url=source_url or "https://weworkremotely.com/remote-jobs.rss")
            elif st == "api":
                primary_source = APIJobSource(url=source_url or "https://arbeitnow.com/api/job-board-api")
            elif st.startswith("mock"):
                mode = "standard"
                if "duplicates" in st:
                    mode = "with_duplicates"
                elif "malformed" in st:
                    mode = "with_malformed"
                elif "failure" in st:
                    mode = "failure"
                primary_source = MockJobSource(mode=mode)

        pipeline = IngestionPipeline(db, primary_source=primary_source)
        return pipeline.run()

    @staticmethod
    def get_runs(db: Session, page: int = 1, limit: int = 10) -> Tuple[List[IngestionRun], int]:
        query = db.query(IngestionRun)
        total = query.count()
        offset = (page - 1) * limit
        runs = query.order_by(desc(IngestionRun.started_at)).offset(offset).limit(limit).all()
        return runs, total

    @staticmethod
    def get_latest_run(db: Session) -> Optional[IngestionRun]:
        return db.query(IngestionRun).order_by(desc(IngestionRun.started_at)).first()

    @staticmethod
    def get_status_summary(db: Session) -> dict:
        latest_run = IngestionService.get_latest_run(db)
        total_jobs = db.query(func.count(Job.id)).scalar() or 0
        active_sources = db.query(Job.source).distinct().count()

        healthy = True
        if latest_run and latest_run.status == "failed":
            healthy = False

        return {
            "last_run": latest_run,
            "total_jobs": total_jobs,
            "active_sources": active_sources,
            "healthy": healthy
        }
