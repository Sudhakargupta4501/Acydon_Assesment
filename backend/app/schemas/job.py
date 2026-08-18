from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class RawJobRecord(BaseModel):
    title: Any
    company: Any
    source: Any
    source_url: Any
    external_id: Optional[Any] = None
    location: Optional[Any] = None
    description: Optional[Any] = None
    employment_type: Optional[Any] = None
    salary: Optional[Any] = None
    posted_at: Optional[Any] = None
    skills: Optional[Any] = None
    remote: Optional[Any] = None

class NormalizedJobCreate(BaseModel):
    external_id: Optional[str] = None
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    location: Optional[str] = "Unknown"
    description: Optional[str] = "No description provided."
    employment_type: Optional[str] = "Full-time"
    salary: Optional[str] = "Not Specified"
    source: str = Field(..., min_length=1)
    source_url: str = Field(..., min_length=1)
    posted_at: Optional[datetime] = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    skills: List[str] = Field(default_factory=list)
    remote: bool = False
    status: str = "active"
    content_hash: str

class JobResponse(BaseModel):
    id: str
    external_id: Optional[str] = None
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    employment_type: Optional[str] = None
    salary: Optional[str] = None
    source: str
    source_url: str
    posted_at: Optional[datetime] = None
    collected_at: datetime
    skills: List[str] = []
    remote: bool
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobListResponse(BaseModel):
    total: int
    page: int
    limit: int
    pages: int
    jobs: List[JobResponse]

class IngestionRunResponse(BaseModel):
    id: str
    source: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str
    records_fetched: int
    records_inserted: int
    records_skipped: int
    records_failed: int
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class IngestionRunListResponse(BaseModel):
    total: int
    page: int
    limit: int
    runs: List[IngestionRunResponse]

class IngestionStatusSummary(BaseModel):
    last_run: Optional[IngestionRunResponse] = None
    total_jobs: int
    active_sources: int
    healthy: bool

class SystemHealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
    active_sources: List[str]
    last_ingestion_status: str
