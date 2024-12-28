from .base import Settings


class DevSettings(Settings):
    LOG_LEVEL: str = "DEBUG"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config(Settings.Config):
        env_file = ".env.dev"


dev_settings = DevSettings()
