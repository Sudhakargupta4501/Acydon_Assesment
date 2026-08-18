import re
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from email.utils import parsedate_to_datetime

class DataNormalizer:
    """
    Normalizes raw job fields into consistent data types, text encodings,
    work mode flags, and standardized date structures.
    """

    @staticmethod
    def normalize_string(val: Optional[Any], default: str = "") -> str:
        if not val or not isinstance(val, str):
            return default
        cleaned = re.sub(r'\s+', ' ', val).strip()
        return cleaned if cleaned else default

    @staticmethod
    def normalize_remote(location_str: str, raw_remote: Optional[Any] = None) -> bool:
        if isinstance(raw_remote, bool):
            return raw_remote
        if isinstance(raw_remote, str) and raw_remote.lower() in ["true", "1", "yes", "remote"]:
            return True
        loc_lower = (location_str or "").lower()
        remote_keywords = ["remote", "work from home", "anywhere", "telecommute", "distributed", "wfh"]
        return any(kw in loc_lower for kw in remote_keywords)

    @staticmethod
    def normalize_employment_type(raw_type: Optional[Any]) -> str:
        if not raw_type or not isinstance(raw_type, str):
            return "Full-time"
        
        t_lower = raw_type.lower()
        if any(k in t_lower for k in ["contract", "freelance", "temp"]):
            return "Contract"
        elif any(k in t_lower for k in ["part", "part-time", "pt"]):
            return "Part-time"
        elif any(k in t_lower for k in ["intern", "trainee"]):
            return "Internship"
        return "Full-time"

    @staticmethod
    def normalize_date(raw_date: Optional[Any]) -> Optional[datetime]:
        if not raw_date:
            return datetime.utcnow()
        if isinstance(raw_date, datetime):
            return raw_date
        if isinstance(raw_date, (int, float)):
            try:
                return datetime.utcfromtimestamp(raw_date)
            except Exception:
                return datetime.utcnow()
        
        date_str = str(raw_date).strip()
        try:
            # Try RFC 2822 (RSS pubDate)
            return parsedate_to_datetime(date_str)
        except Exception:
            pass

        # Try common ISO 8601 patterns
        iso_patterns = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d"
        ]
        for fmt in iso_patterns:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        return datetime.utcnow()

    @staticmethod
    def normalize_skills(raw_skills: Optional[Any]) -> List[str]:
        if not raw_skills:
            return []
        if isinstance(raw_skills, list):
            skills = [str(s).strip() for s in raw_skills if s]
            return list(set(skills))
        if isinstance(raw_skills, str):
            parts = re.split(r'[,|/;]', raw_skills)
            return list(set([p.strip() for p in parts if p.strip()]))
        return []

    @classmethod
    def generate_fingerprint(cls, title: str, company: str, location: str, source_url: str) -> str:
        """Generates SHA-256 hash fingerprint of normalized identifying fields."""
        payload = f"{title.lower()}|{company.lower()}|{location.lower()}|{source_url.lower()}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    @classmethod
    def normalize_record(cls, raw: Dict[str, Any], default_source: str = "Unknown") -> Dict[str, Any]:
        title = cls.normalize_string(raw.get("title"), default="")
        company = cls.normalize_string(raw.get("company"), default="")
        location = cls.normalize_string(raw.get("location"), default="Remote")
        source = cls.normalize_string(raw.get("source"), default=default_source)
        source_url = cls.normalize_string(raw.get("source_url"), default="")
        external_id = cls.normalize_string(raw.get("external_id"), default=None) or None
        description = cls.normalize_string(raw.get("description"), default="No description provided.")
        employment_type = cls.normalize_employment_type(raw.get("employment_type"))
        salary = cls.normalize_string(raw.get("salary"), default="Not Specified")
        posted_at = cls.normalize_date(raw.get("posted_at"))
        skills = cls.normalize_skills(raw.get("skills"))
        remote = cls.normalize_remote(location, raw.get("remote"))

        content_hash = cls.generate_fingerprint(title, company, location, source_url or external_id or title)

        return {
            "external_id": external_id,
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "employment_type": employment_type,
            "salary": salary,
            "source": source,
            "source_url": source_url,
            "posted_at": posted_at,
            "collected_at": datetime.utcnow(),
            "skills": skills,
            "remote": remote,
            "status": "active",
            "content_hash": content_hash
        }
