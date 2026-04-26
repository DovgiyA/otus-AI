"""
Application configuration settings.
Loads environment variables with fallbacks for local development.
Supports both PostgreSQL (preferred) and SQLite (fallback).
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database - tries PostgreSQL first, falls back to SQLite
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./survey.db"  # Fallback to SQLite for local development
    )
    
    # For PostgreSQL, use: postgresql://user:password@localhost:5432/mini_survey_db
    # For SQLite, use: sqlite:///./survey.db (relative) or sqlite:////tmp/survey.db (absolute)
    
    # API
    API_TITLE: str = "Mini Survey API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
