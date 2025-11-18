# src/api/core/config/dev.py
from typing import List

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from .base import ApiSettings


class Settings(ApiSettings):
    """Development-specific settings that override base configuration"""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        description="Allowed CORS origins for development",
    )

    # Dev database URL as a plain string
    DATABASE_URL: str = "postgresql+asyncpg://dev_user:dev_password@localhost:5432/chatbot_dev"

    # Dev-specific config (e.g. different env file)
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=True,
        extra="ignore",
    )
