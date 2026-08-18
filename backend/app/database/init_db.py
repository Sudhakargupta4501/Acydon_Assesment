from app.database.connection import engine, Base
from app.models.job import Job, IngestionRun, IngestionError
from app.utils.logger import logger

def init_db():
    logger.info("Initializing database schemas...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schemas initialized successfully.")

if __name__ == "__main__":
    init_db()
