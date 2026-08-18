from datetime import datetime
from app.ingestion.normalizer import DataNormalizer

def test_normalize_string():
    assert DataNormalizer.normalize_string("  React   Developer  ") == "React Developer"
    assert DataNormalizer.normalize_string(None, default="Unknown") == "Unknown"
    assert DataNormalizer.normalize_string("", default="N/A") == "N/A"

def test_normalize_remote():
    assert DataNormalizer.normalize_remote("Remote - Worldwide") is True
    assert DataNormalizer.normalize_remote("San Francisco, CA", raw_remote=True) is True
    assert DataNormalizer.normalize_remote("New York, NY", raw_remote=False) is False
    assert DataNormalizer.normalize_remote("Work From Home") is True

def test_normalize_employment_type():
    assert DataNormalizer.normalize_employment_type("FULL_TIME") == "Full-time"
    assert DataNormalizer.normalize_employment_type("Contractor") == "Contract"
    assert DataNormalizer.normalize_employment_type("part time") == "Part-time"
    assert DataNormalizer.normalize_employment_type(None) == "Full-time"

def test_normalize_date():
    dt = DataNormalizer.normalize_date("2026-08-18T10:00:00Z")
    assert isinstance(dt, datetime)
    assert dt.year == 2026

def test_generate_fingerprint():
    h1 = DataNormalizer.generate_fingerprint("Software Engineer", "Acme", "Remote", "https://example.com/job1")
    h2 = DataNormalizer.generate_fingerprint("software engineer", "ACME", "remote", "HTTPS://EXAMPLE.COM/JOB1")
    assert h1 == h2

def test_normalize_record():
    raw = {
        "title": " Frontend Developer ",
        "company": " TechCorp ",
        "location": " Remote ",
        "source": " TestSource ",
        "source_url": " https://example.com/1 ",
        "skills": "React, TypeScript, CSS"
    }
    norm = DataNormalizer.normalize_record(raw)
    assert norm["title"] == "Frontend Developer"
    assert norm["company"] == "TechCorp"
    assert norm["remote"] is True
    assert set(norm["skills"]) == {"React", "TypeScript", "CSS"}
    assert "content_hash" in norm
