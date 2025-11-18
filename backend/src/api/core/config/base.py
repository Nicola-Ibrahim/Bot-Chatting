# src/api/core/config/base.py
from typing import Any, ClassVar, List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logging import LoggingConfig


class ApiSettings(BaseSettings):
    """Main application settings with environment-aware configuration"""

    # Pydantic v2-style config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=True,
        extra="ignore",
    )

    # Application Metadata
    PROJECT_NAME: str = "Chatbot Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    DESCRIPTION: str = "API service for chatbot application."

    # Security
    SECRET_KEY: str = "change-me-in-production"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | list[str] = []

    # Simple database URL string (instead of PostgresDsn + validator)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot"

    # Logging
    LOGGING: ClassVar[LoggingConfig] = LoggingConfig()

    def configure(self) -> None:
        """Apply all configurations"""
        if self.DEBUG:
            self.LOGGING.LOG_LEVEL = "DEBUG"
        self.LOGGING.configure_logging()
