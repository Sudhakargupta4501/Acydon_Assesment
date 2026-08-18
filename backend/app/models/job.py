import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    external_id = Column(String(255), nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    employment_type = Column(String(100), nullable=True)
    salary = Column(String(255), nullable=True)
    source = Column(String(100), nullable=False, index=True)
    source_url = Column(Text, nullable=False)
    posted_at = Column(DateTime, nullable=True)
    collected_at = Column(DateTime, default=datetime.utcnow)
    skills = Column(JSON, nullable=True)
    remote = Column(Boolean, default=False, index=True)
    status = Column(String(50), default="active")
    content_hash = Column(String(64), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(100), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="running")  # running, success, partial_success, failed
    records_fetched = Column(Integer, default=0)
    records_inserted = Column(Integer, default=0)
    records_skipped = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

class IngestionError(Base):
    __tablename__ = "ingestion_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String(36), nullable=False, index=True)
    raw_record = Column(Text, nullable=True)
    error_reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
