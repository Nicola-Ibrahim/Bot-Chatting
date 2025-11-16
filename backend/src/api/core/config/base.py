from typing import Any, ClassVar

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logging import LoggingConfig


class AppSettings(BaseSettings):
    """Main application settings with environment-aware configuration"""

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

    # Security
    SECRET_KEY: str = "change-me-in-production"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "chatbot"
    DATABASE_URI: PostgresDsn | None = None

    # Logging
    LOGGING: ClassVar[LoggingConfig] = LoggingConfig()

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            if v.startswith("["):
                import json

                return json.loads(v)
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_uri(cls, v: str | None, values: dict[str, Any]) -> PostgresDsn:
        """Construct DB URI if not explicitly provided"""
        if v:
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["POSTGRES_HOST"],
            port=str(values["POSTGRES_PORT"]),
            path=values["POSTGRES_DB"],
        )

    def configure(self) -> None:
        """Apply all configurations"""
        if self.DEBUG:
            self.LOGGING.LOG_LEVEL = "DEBUG"
        self.LOGGING.configure_logging()
