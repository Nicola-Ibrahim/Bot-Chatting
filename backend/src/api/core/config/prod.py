import secrets
from typing import List, Optional

from pydantic import Field, PostgresDsn, RedisDsn

from .base import ApiSettings


class ProdSettings(ApiSettings):
    """Production environment settings with security-hardened defaults"""

    # Environment identification
    ENVIRONMENT: str = "production"

    # Security-critical overrides
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(64), description="Cryptographic secret for session security"
    )

    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["https://your-production-domain.com"], description="Allowed origins for production environment"
    )

    # Database configuration
    POSTGRES_HOST: str = "production-db-host"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "prod_db_user"
    POSTGRES_PASSWORD: str = Field(..., description="Database password (must be set via env var)", min_length=16)
    DATABASE_URI: Optional[PostgresDsn] = None

    # Redis/cache configuration
    REDIS_URL: RedisDsn = Field(
        default="redis://production-redis:6379/0", description="Redis connection URL for caching"
    )

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    class Config(ApiSettings.Config):
        env_file = ".env.prod"
        env_file_encoding = "utf-8"
        extra = "forbid"  # Strict validation in production

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Constructs SQLAlchemy-compatible async DB URI"""
        return (
            str(self.DATABASE_URI)
            if self.DATABASE_URI
            else f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
