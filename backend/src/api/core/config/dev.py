from typing import List

from pydantic import Field

from .base import AppSettings


class Settings(AppSettings):
    """Development-specific settings that override base configuration"""

    # Override base defaults for development
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"], description="Allowed CORS origins for development"
    )

    # Development-specific database configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "dev_user"
    POSTGRES_PASSWORD: str = "dev_password"
    POSTGRES_DB: str = "chatbot_dev"

    class Config(AppSettings.Config):
        env_file = ".env.dev"
        extra = "allow"  # More forgiving during development
