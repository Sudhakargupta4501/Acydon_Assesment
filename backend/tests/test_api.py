import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base, get_db
from app.models.job import Job, IngestionRun, IngestionError  # Import models so Base.metadata knows about them!
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in static pool memory DB
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["Operational", "Degraded"]
    assert data["database"] == "Operational"

def test_trigger_ingestion_api():
    response = client.post("/api/ingestion/run?source_type=mock")
    assert response.status_code == 200
    data = response.json()
    assert data["records_inserted"] == 3
    assert data["status"] == "success"

def test_get_jobs_api():
    response = client.get("/api/jobs?q=React")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "React" in data["jobs"][0]["title"]

def test_get_ingestion_status_api():
    response = client.get("/api/ingestion/status")
    assert response.status_code == 200
    data = response.json()
    assert "healthy" in data
    assert "total_jobs" in data
