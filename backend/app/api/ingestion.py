from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.job import IngestionRunResponse, IngestionRunListResponse, IngestionStatusSummary
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/api/ingestion", tags=["Ingestion"])

@router.post("/run", response_model=IngestionRunResponse, summary="Trigger manual job data ingestion run")
def trigger_ingestion(
    source_type: Optional[str] = Query(None, description="Source adapter type (rss, api, mock, mock_duplicates, mock_malformed, mock_failure)"),
    source_url: Optional[str] = Query(None, description="Custom feed/API URL"),
    db: Session = Depends(get_db)
):
    run_record = IngestionService.trigger_run(db, source_type=source_type, source_url=source_url)
    return IngestionRunResponse.model_validate(run_record)

@router.get("/status", response_model=IngestionStatusSummary, summary="Get current ingestion pipeline health summary")
def get_ingestion_status(db: Session = Depends(get_db)):
    summary = IngestionService.get_status_summary(db)
    last_run_dto = IngestionRunResponse.model_validate(summary["last_run"]) if summary["last_run"] else None
    return IngestionStatusSummary(
        last_run=last_run_dto,
        total_jobs=summary["total_jobs"],
        active_sources=summary["active_sources"],
        healthy=summary["healthy"]
    )

@router.get("/runs", response_model=IngestionRunListResponse, summary="Get paginated history of ingestion runs")
def get_ingestion_runs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    runs, total = IngestionService.get_runs(db, page=page, limit=limit)
    return IngestionRunListResponse(
        total=total,
        page=page,
        limit=limit,
        runs=[IngestionRunResponse.model_validate(r) for r in runs]
    )
