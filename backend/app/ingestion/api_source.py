from typing import List, Dict, Any
from app.ingestion.base import JobSource
from app.utils.retry import SafeHttpClient
from app.utils.logger import logger

class APIJobSource(JobSource):
    def __init__(self, url: str = "https://arbeitnow.com/api/job-board-api", source_name: str = "Arbeitnow Public API"):
        self.url = url
        self._source_name = source_name
        self.client = SafeHttpClient()

    @property
    def source_name(self) -> str:
        return self._source_name

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        logger.info(f"Fetching REST API jobs from: {self.url}")
        response = self.client.fetch(self.url)
        data = response.json()

        # Handle different API response root structures
        items = []
        if isinstance(data, dict):
            items = data.get("data") or data.get("jobs") or data.get("results") or []
        elif isinstance(data, list):
            items = data

        jobs = []
        for item in items:
            if not isinstance(item, dict):
                continue
            
            raw_record = {
                "title": item.get("title") or item.get("job_title"),
                "company": item.get("company_name") or item.get("company"),
                "source": self.source_name,
                "source_url": item.get("url") or item.get("link") or item.get("job_url"),
                "external_id": str(item.get("slug") or item.get("id") or item.get("url", "")),
                "location": item.get("location") or ("Remote" if item.get("remote") else "On-site"),
                "description": item.get("description"),
                "employment_type": ", ".join(item.get("job_types", [])) if isinstance(item.get("job_types"), list) else item.get("job_type"),
                "posted_at": item.get("created_at"),
                "skills": item.get("tags") if isinstance(item.get("tags"), list) else [],
                "remote": bool(item.get("remote")) if "remote" in item else True
            }
            jobs.append(raw_record)

        logger.info(f"Successfully fetched {len(jobs)} raw job records from REST API.")
        return jobs
