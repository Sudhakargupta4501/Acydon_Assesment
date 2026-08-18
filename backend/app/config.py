import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "JobFlow Ingestion Platform"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./jobflow.db"
    
    # Ingestion Configuration
    REQUEST_TIMEOUT: int = 10
    MIN_REQUEST_INTERVAL: int = 2
    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: float = 2.0
    
    # Sources
    PRIMARY_SOURCE_TYPE: str = "rss"
    PRIMARY_SOURCE_URL: str = "https://weworkremotely.com/remote-jobs.rss"
    FALLBACK_SOURCE_TYPE: str = "api"
    FALLBACK_SOURCE_URL: str = "https://arbeitnow.com/api/job-board-api"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
