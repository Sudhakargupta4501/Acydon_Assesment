from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.mock_source import MockJobSource

def test_pipeline_standard_run():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    source = MockJobSource(mode="standard")
    pipeline = IngestionPipeline(db=db, primary_source=source)
    run_record = pipeline.run()

    assert run_record.status == "success"
    assert run_record.records_fetched == 3
    assert run_record.records_inserted == 3
    assert run_record.records_skipped == 0
    assert run_record.records_failed == 0

    db.close()

def test_pipeline_duplicates_run():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    source = MockJobSource(mode="with_duplicates")
    pipeline = IngestionPipeline(db=db, primary_source=source)
    run_record = pipeline.run()

    assert run_record.status == "success"
    assert run_record.records_fetched == 5
    assert run_record.records_inserted == 3
    assert run_record.records_skipped == 2

    db.close()

def test_pipeline_malformed_run():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    source = MockJobSource(mode="with_malformed")
    pipeline = IngestionPipeline(db=db, primary_source=source)
    run_record = pipeline.run()

    assert run_record.status == "partial_success"
    assert run_record.records_fetched == 5
    assert run_record.records_failed == 2

    db.close()

def test_pipeline_fallback_activation():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    primary_failing = MockJobSource(mode="failure")
    fallback_ok = MockJobSource(mode="standard")

    pipeline = IngestionPipeline(db=db, primary_source=primary_failing, fallback_source=fallback_ok)
    run_record = pipeline.run()

    assert run_record.status == "success"
    assert "Fallback" in run_record.source
    assert run_record.records_inserted == 3

    db.close()
