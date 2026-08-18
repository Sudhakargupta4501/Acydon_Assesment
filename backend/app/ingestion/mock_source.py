import time
from typing import List, Dict, Any
from app.ingestion.base import JobSource
from app.utils.logger import logger

class MockJobSource(JobSource):
    """
    Mock/Sandbox Job Source Adapter for offline execution, integration testing,
    and chaos simulation (malformed records, duplicates, schema anomalies).
    """
    def __init__(self, mode: str = "standard", source_name: str = "Sandbox Mock Source"):
        self.mode = mode
        self._source_name = source_name

    @property
    def source_name(self) -> str:
        return self._source_name

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        logger.info(f"Executing MockJobSource in '{self.mode}' mode...")

        if self.mode == "failure":
            raise Exception("Simulated connection timeout / source unavailable in MockJobSource.")

        base_jobs = [
            {
                "external_id": "mock-001",
                "title": " Senior React / Next.js Engineer ",
                "company": " Acdyon Technologies ",
                "location": " Remote - Worldwide ",
                "description": "<p>Build high-performance <strong>ingestion & web data platforms</strong>.</p>",
                "employment_type": "Full-time",
                "salary": "$120,000 - $150,000 USD",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/mock-001",
                "posted_at": "2026-08-18T10:00:00Z",
                "skills": ["React", "TypeScript", "Tailwind CSS", "Next.js"],
                "remote": True
            },
            {
                "external_id": "mock-002",
                "title": "Backend Python FastAPI Specialist",
                "company": "CloudData Systems",
                "location": "San Francisco, CA (Hybrid)",
                "description": "Architect scalable async FastAPI backend microservices and SQLAlchemy pipelines.",
                "employment_type": "FULL_TIME",
                "salary": "$140k - $170k",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/mock-002",
                "posted_at": "2026-08-17T15:30:00Z",
                "skills": ["Python", "FastAPI", "PostgreSQL", "Pydantic", "SQLAlchemy"],
                "remote": False
            },
            {
                "external_id": "mock-003",
                "title": "DevOps & Data Platform Architect",
                "company": "StreamLine Infrastructure",
                "location": "Berlin, Germany",
                "description": "Manage Kubernetes clusters, PostgreSQL Neon DB instances, and GitHub Actions CI/CD pipelines.",
                "employment_type": "contract",
                "salary": "€80 - €100 / hr",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/mock-003",
                "posted_at": "2026-08-16T09:15:00Z",
                "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"],
                "remote": True
            }
        ]

        if self.mode == "with_duplicates":
            # Add duplicates to test deduplication
            base_jobs.append({
                "external_id": "mock-001",  # Duplicate external_id
                "title": "Senior React / Next.js Engineer",
                "company": "Acdyon Technologies",
                "location": "Remote",
                "description": "Duplicate post",
                "employment_type": "Full-time",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/mock-001",
                "posted_at": "2026-08-18T10:00:00Z",
                "skills": ["React"],
                "remote": True
            })
            base_jobs.append({
                # No external_id, matching title + company + location + source_url fingerprint
                "title": "Backend Python FastAPI Specialist",
                "company": "CloudData Systems",
                "location": "San Francisco, CA (Hybrid)",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/mock-002",
                "description": "Fingerprint match duplicate",
                "skills": ["Python"],
                "remote": False
            })

        if self.mode == "with_malformed":
            # Add invalid records missing required fields (title or company)
            base_jobs.append({
                "external_id": "bad-001",
                "title": "",  # Empty title -> Invalid!
                "company": "No Title Corp",
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/bad-001"
            })
            base_jobs.append({
                "external_id": "bad-002",
                "title": "Missing Company Job",
                "company": "",  # Empty company -> Invalid!
                "source": self.source_name,
                "source_url": "https://sandbox.acdyon.dev/jobs/bad-002"
            })

        return base_jobs
