"""
Configuration settings for the application.

This module uses Pydantic's BaseSettings for environment variable validation.
"""

import json
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # CORS origins
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Construct PostgreSQL connection string."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Project settings
    PROJECT_NAME: str = "LinkedIn CRM"

    # LinkedIn settings
    LINKEDIN_USERNAME: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    LINKEDIN_LI_AT: Optional[str] = None
    LINKEDIN_JSESSIONID: Optional[str] = None

    # Redis settings (for background tasks)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Log level
    LOG_LEVEL: str = "INFO"

    class Config:
        """Pydantic config for settings."""

        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create settings instance
settings = Settings()