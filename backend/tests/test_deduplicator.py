from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.ingestion.normalizer import DataNormalizer
from app.ingestion.validator import RecordValidator
from app.ingestion.deduplicator import Deduplicator

def test_deduplicator():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    raw1 = {
        "external_id": "job-1",
        "title": "Data Engineer",
        "company": "DataCorp",
        "source": "Mock",
        "source_url": "https://example.com/1"
    }
    raw2 = {
        "external_id": "job-1",  # Duplicate external_id
        "title": "Data Engineer",
        "company": "DataCorp",
        "source": "Mock",
        "source_url": "https://example.com/1"
    }
    raw3 = {
        "external_id": "job-2",
        "title": "Frontend Engineer",
        "company": "WebCorp",
        "source": "Mock",
        "source_url": "https://example.com/2"
    }

    rec1, _ = RecordValidator.validate(DataNormalizer.normalize_record(raw1))
    rec2, _ = RecordValidator.validate(DataNormalizer.normalize_record(raw2))
    rec3, _ = RecordValidator.validate(DataNormalizer.normalize_record(raw3))

    records = [rec1, rec2, rec3]
    unique, skipped = Deduplicator.filter_batch(records, db)

    assert len(unique) == 2
    assert skipped == 1
    assert unique[0].external_id == "job-1"
    assert unique[1].external_id == "job-2"

    db.close()
