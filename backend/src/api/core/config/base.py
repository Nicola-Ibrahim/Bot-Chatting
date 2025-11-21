# src/api/core/config/base.py
import logging.config
from typing import Any

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # Security
    SECRET_KEY: str = "change-me-in-production"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | list[str] = []

    # Simple database URL string (instead of PostgresDsn + validator)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot"
    ACCOUNTS_ENABLE_REGISTRATION: bool = True
    ACCOUNTS_DEFAULT_ROLE: str = "user"
    CHATS_MAX_ACTIVE_CHATS_PER_USER: int = 5

    # Logging defaults (overridable per environment)
    LOGGER_NAME: str = "chatbot"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s"
    LOG_DATEFMT: str = "%Y-%m-%d %H:%M:%S"
    LOG_USE_COLORS: bool = True
    LOG_USE_JSON: bool = False

    def configure(self) -> None:
        """Apply all configurations"""
        log_level = "DEBUG" if self.DEBUG else self.LOG_LEVEL
        logging.config.dictConfig(self.logging_dict_config(log_level))

    def logging_dict_config(self, log_level: str) -> dict[str, Any]:
        """Return dictConfig ready logging configuration for the environment."""
        formatter_name = "json" if self.LOG_USE_JSON else "default"
        handler_name = "json_console" if self.LOG_USE_JSON else "console"

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": self.LOG_FORMAT,
                    "datefmt": self.LOG_DATEFMT,
                    "use_colors": self.LOG_USE_COLORS,
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": self.LOG_FORMAT,
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "json_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                self.LOGGER_NAME: {
                    "handlers": [handler_name],
                    "level": log_level,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": [handler_name],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
