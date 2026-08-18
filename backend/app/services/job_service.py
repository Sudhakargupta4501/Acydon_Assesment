from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from app.models.job import Job

class JobService:
    @staticmethod
    def get_jobs(
        db: Session,
        search_query: Optional[str] = None,
        location: Optional[str] = None,
        remote: Optional[bool] = None,
        employment_type: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[List[Job], int, int]:
        query = db.query(Job)

        # Full-text search across Title, Company, Location, Description
        if search_query and search_query.strip():
            sq = f"%{search_query.strip()}%"
            query = query.filter(
                or_(
                    Job.title.ilike(sq),
                    Job.company.ilike(sq),
                    Job.location.ilike(sq),
                    Job.description.ilike(sq)
                )
            )

        if location and location.strip():
            query = query.filter(Job.location.ilike(f"%{location.strip()}%"))

        if remote is not None:
            query = query.filter(Job.remote == remote)

        if employment_type and employment_type.strip():
            query = query.filter(Job.employment_type.ilike(f"%{employment_type.strip()}%"))

        if company and company.strip():
            query = query.filter(Job.company.ilike(f"%{company.strip()}%"))

        if source and source.strip():
            query = query.filter(Job.source.ilike(f"%{source.strip()}%"))

        total_records = query.count()
        total_pages = (total_records + limit - 1) // limit if limit > 0 else 1

        offset = (page - 1) * limit
        jobs = query.order_by(desc(Job.posted_at), desc(Job.created_at)).offset(offset).limit(limit).all()

        return jobs, total_records, total_pages

    @staticmethod
    def get_job_by_id(db: Session, job_id: str) -> Optional[Job]:
        return db.query(Job).filter(Job.id == job_id).first()
