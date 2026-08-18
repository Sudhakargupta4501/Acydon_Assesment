import feedparser
from typing import List, Dict, Any
from app.ingestion.base import JobSource
from app.utils.retry import SafeHttpClient
from app.utils.logger import logger

class RSSJobSource(JobSource):
    def __init__(self, url: str = "https://weworkremotely.com/remote-jobs.rss", source_name: str = "WeWorkRemotely RSS"):
        self.url = url
        self._source_name = source_name
        self.client = SafeHttpClient()

    @property
    def source_name(self) -> str:
        return self._source_name

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        logger.info(f"Fetching RSS feed from: {self.url}")
        response = self.client.fetch(self.url)
        
        feed = feedparser.parse(response.text)
        if feed.bozo:
            logger.warning(f"Feedparser warning for {self.url}: {feed.bozo_exception}")

        jobs = []
        for entry in feed.entries:
            # Map RSS feed fields to internal raw record structure
            raw_record = {
                "title": getattr(entry, "title", None),
                "company": getattr(entry, "author", None) or getattr(entry, "category", None) or "WeWorkRemotely Partner",
                "source": self.source_name,
                "source_url": getattr(entry, "link", getattr(entry, "id", "")),
                "external_id": getattr(entry, "id", getattr(entry, "link", None)),
                "location": "Remote",  # WeWorkRemotely is default remote
                "description": getattr(entry, "summary", getattr(entry, "description", None)),
                "employment_type": getattr(entry, "category", "Full-time"),
                "posted_at": getattr(entry, "published", getattr(entry, "updated", None)),
                "skills": [cat.get("term") for cat in getattr(entry, "tags", []) if isinstance(cat, dict) and cat.get("term")],
                "remote": True
            }
            jobs.append(raw_record)

        logger.info(f"Successfully fetched {len(jobs)} raw job records from RSS feed.")
        return jobs
