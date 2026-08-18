from typing import List, Tuple, Set
from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import NormalizedJobCreate
from app.utils.logger import logger

class Deduplicator:
    """
    Suppresses duplicate job listings using a dual-layered strategy:
    1. Primary key match on (source + external_id)
    2. Fallback cryptographic fingerprint hash (content_hash)
    """

    @staticmethod
    def is_duplicate(
        record: NormalizedJobCreate,
        db: Session,
        seen_batch_hashes: Set[str],
        seen_batch_ext_ids: Set[str]
    ) -> bool:
        # Check within current batch memory first
        if record.content_hash in seen_batch_hashes:
            return True

        if record.external_id and f"{record.source}:{record.external_id}" in seen_batch_ext_ids:
            return True

        # Check DB for content_hash
        existing_by_hash = db.query(Job.id).filter(Job.content_hash == record.content_hash).first()
        if existing_by_hash:
            return True

        # Check DB for external_id + source
        if record.external_id:
            existing_by_ext = db.query(Job.id).filter(
                Job.source == record.source,
                Job.external_id == record.external_id
            ).first()
            if existing_by_ext:
                return True

        return False

    @classmethod
    def filter_batch(
        cls,
        records: List[NormalizedJobCreate],
        db: Session
    ) -> Tuple[List[NormalizedJobCreate], int]:
        """
        Filters a list of normalized job records, discarding duplicates.
        Returns (unique_records, count_skipped_duplicates).
        """
        unique_records: List[NormalizedJobCreate] = []
        seen_batch_hashes: Set[str] = set()
        seen_batch_ext_ids: Set[str] = set()
        skipped_count = 0

        for record in records:
            if cls.is_duplicate(record, db, seen_batch_hashes, seen_batch_ext_ids):
                skipped_count += 1
                logger.debug(f"Skipping duplicate record: '{record.title}' @ '{record.company}'")
            else:
                unique_records.append(record)
                seen_batch_hashes.add(record.content_hash)
                if record.external_id:
                    seen_batch_ext_ids.add(f"{record.source}:{record.external_id}")

        return unique_records, skipped_count
