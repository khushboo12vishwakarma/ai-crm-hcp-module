"""Application configuration loaded from environment variables."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from .env file."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./crm.db"
    
    # Groq Configuration (will be used in Phase 2)
    GROQ_API_KEY: str = ""
    GROQ_MODEL_PRIMARY: str = "gemma2-9b-it"
    GROQ_MODEL_BACKUP: str = "llama-3.3-70b-versatile"
    
    # Server
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    """Get cached settings instance."""
    return Settings()
