from .base import Settings


class ProdSettings(Settings):
    LOG_LEVEL: str = "INFO"
    BACKEND_CORS_ORIGINS: list[str] = ["https://your-production-domain.com"]

    class Config(Settings.Config):
        env_file = ".env.prod"


prod_settings = ProdSettings()
