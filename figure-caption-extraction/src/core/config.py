from typing import Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    # API settings
    api_key: str
    api_host: str = "0.0.0.0"
    api_port: str = "8000"
    
    # Database settings
    DB_PATH: str = "data/figures.db"  # Changed to match .env variable name
    
    # PubTator settings
    PUBTATOR_API_URL: str
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600
    
    # Application settings
    log_level: str = "INFO"
    # Default source with room for expansion
    ACTIVE_SOURCE: str = "pubmed"  # Default to PubMed
    
    # Batch processing settings
    WATCH_FOLDER: str = "data/watch"
    BATCH_SIZE: int = 100
    BATCH_TIMEOUT: int = 3600
    BATCH_RETRY_COUNT: int = 3
    
    # Success/Failure status
    EXIT_SUCCESS: int = 0
    EXIT_FAILURE: int = 1
    
    # Logging settings
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "data/logs/ingestion.log"
    
    class Config:
        env_file = ".env"

settings = Settings()