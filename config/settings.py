"""
PhishCLI - Application Configuration Engine
Uses pydantic-settings to manage environment variables, API keys, and operational flags.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from config.constants import APP_DIR, DB_PATH


class Settings(BaseSettings):
    """Global Application Settings populated from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Environment
    ENV: str = Field(default="production", description="Environment: development, testing, production")
    DEBUG: bool = Field(default=False, description="Enable debug verbosity")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")

    # Database Settings
    DATABASE_URL: str = Field(
        default=f"sqlite:///{DB_PATH}",
        description="SQLAlchemy compatible database URL",
    )

    # External Threat Intelligence APIs
    VIRUSTOTAL_API_KEY: Optional[str] = Field(default=None, description="cac92775fab9c184875bbf8422fc01e824817a6e282985bd0574b1ae6e5278d3")
    ABUSEIPDB_API_KEY: Optional[str] = Field(default=None, description="8215c3ee23a5ffcd13fa52709737d648a6f1e3eb647b4b489f242f58002acbf1163a513ebaa5e301")

    # OAuth Settings
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth Client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth Client Secret")

    # Timeouts & Limits
    HTTP_TIMEOUT_SECONDS: int = Field(default=10, description="HTTP client request timeout in seconds")
    MAX_EMAIL_FETCH_LIMIT: int = Field(default=500, description="Maximum emails allowed per batch fetch")


# Singleton instance
settings = Settings()