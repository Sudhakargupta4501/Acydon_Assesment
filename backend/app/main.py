from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.database.connection import SessionLocal
from app.database.init_db import init_db
from app.api import jobs, ingestion, health
from app.services.ingestion_service import IngestionService
from app.models.job import Job
from app.utils.logger import logger

def scheduled_ingestion_task():
    logger.info("Executing automated scheduled background ingestion...")
    db = SessionLocal()
    try:
        IngestionService.trigger_run(db)
    except Exception as exc:
        logger.error(f"Scheduled ingestion task error: {exc}")
    finally:
        db.close()

scheduler = BackgroundScheduler(daemon=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Starting JobFlow Ingestion Service backend...")
    init_db()

    # Seed initial batch if DB is empty
    db = SessionLocal()
    try:
        job_count = db.query(Job).count()
        if job_count == 0:
            logger.info("Database is empty on startup. Triggering initial ingestion run...")
            IngestionService.trigger_run(db, source_type="mock")
            # Also attempt primary public source
            try:
                IngestionService.trigger_run(db, source_type="rss")
            except Exception as e:
                logger.warning(f"Initial RSS fetch skipped: {e}")
    finally:
        db.close()

    # Start periodic background scheduler (every 60 minutes)
    scheduler.add_job(scheduled_ingestion_task, 'interval', minutes=60, id='job_ingestion_cron', replace_existing=True)
    scheduler.start()
    logger.info("APScheduler started: Periodic background job ingestion active (60m interval).")

    yield

    # Shutdown tasks
    logger.info("Shutting down background scheduler and API...")
    if scheduler.running:
        scheduler.shutdown(wait=False)

app = FastAPI(
    title=settings.APP_NAME,
    description="Production-Quality Job Data Ingestion & Dashboard API with resilient ETL pipeline, source adapters, deduplication, and automated background jobs.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Registration
app.include_router(jobs.router)
app.include_router(ingestion.router)
app.include_router(health.router)

@app.get("/", summary="Root Endpoint")
def root_endpoint():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "documentation": "/docs",
        "health_check": "/api/health"
    }
