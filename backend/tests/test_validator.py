from app.ingestion.validator import RecordValidator
from app.ingestion.normalizer import DataNormalizer

def test_validate_valid_record():
    raw = {
        "title": "Backend Engineer",
        "company": "FastAPI Inc",
        "source": "MockSource",
        "source_url": "https://example.com/job"
    }
    norm = DataNormalizer.normalize_record(raw)
    record, error = RecordValidator.validate(norm)
    assert record is not None
    assert error is None
    assert record.title == "Backend Engineer"

def test_validate_missing_title():
    raw = {
        "title": "",
        "company": "FastAPI Inc",
        "source": "MockSource",
        "source_url": "https://example.com/job"
    }
    norm = DataNormalizer.normalize_record(raw)
    record, error = RecordValidator.validate(norm)
    assert record is None
    assert "title" in error.lower()

def test_validate_missing_company():
    raw = {
        "title": "Backend Engineer",
        "company": "",
        "source": "MockSource",
        "source_url": "https://example.com/job"
    }
    norm = DataNormalizer.normalize_record(raw)
    record, error = RecordValidator.validate(norm)
    assert record is None
    assert "company" in error.lower()
