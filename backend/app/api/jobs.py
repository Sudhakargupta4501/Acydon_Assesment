from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.job import JobListResponse, JobResponse
from app.services.job_service import JobService

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("", response_model=JobListResponse, summary="Get paginated job listings with search & filtering")
def get_jobs(
    q: Optional[str] = Query(None, description="Search term for title, company, description, location"),
    location: Optional[str] = Query(None, description="Filter by location string"),
    remote: Optional[bool] = Query(None, description="Filter by remote flag (true/false)"),
    employment_type: Optional[str] = Query(None, description="Filter by employment type (e.g. Full-time, Contract)"),
    company: Optional[str] = Query(None, description="Filter by company name"),
    source: Optional[str] = Query(None, description="Filter by job source"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    jobs, total, pages = JobService.get_jobs(
        db=db,
        search_query=q,
        location=location,
        remote=remote,
        employment_type=employment_type,
        company=company,
        source=source,
        page=page,
        limit=limit
    )
    return JobListResponse(
        total=total,
        page=page,
        limit=limit,
        pages=pages,
        jobs=[JobResponse.model_validate(j) for j in jobs]
    )

@router.get("/{job_id}", response_model=JobResponse, summary="Get job details by ID")
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    job = JobService.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job listing with ID '{job_id}' not found."
        )
    return JobResponse.model_validate(job)
