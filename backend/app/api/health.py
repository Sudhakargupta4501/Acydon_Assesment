from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.connection import get_db
from app.schemas.job import SystemHealthResponse
from app.services.ingestion_service import IngestionService
from app.config import settings

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("", response_model=SystemHealthResponse, summary="Comprehensive system health diagnostic check")
def health_check(db: Session = Depends(get_db)):
    db_status = "Operational"
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"Degraded: {str(exc)}"

    summary = IngestionService.get_status_summary(db)
    last_status = "No runs recorded"
    if summary["last_run"]:
        last_status = f"{summary['last_run'].status} at {summary['last_run'].started_at.isoformat()}"

    system_status = "Operational" if db_status == "Operational" and summary["healthy"] else "Degraded"

    return SystemHealthResponse(
        status=system_status,
        timestamp=datetime.utcnow(),
        database=db_status,
        active_sources=[settings.PRIMARY_SOURCE_TYPE, settings.FALLBACK_SOURCE_TYPE, "mock"],
        last_ingestion_status=last_status
    )
