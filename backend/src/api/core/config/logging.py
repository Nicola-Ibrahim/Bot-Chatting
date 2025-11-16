import logging.config
from typing import Any

from pydantic_settings import BaseSettings


class LoggingConfig(BaseSettings):
    """Centralized logging configuration with production-ready defaults"""

    LOGGER_NAME: str = "chatbot"
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(message)s"
    LOG_DATEFMT: str = "%Y-%m-%d %H:%M:%S"

    # Pre-configured logging dictConfig
    @property
    def dict_config(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": self.LOG_FORMAT,
                    "datefmt": self.LOG_DATEFMT,
                    "use_colors": True,
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
                    "handlers": ["console"],
                    "level": self.LOG_LEVEL,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }

    def configure_logging(self) -> None:
        """Apply logging configuration"""
        logging.config.dictConfig(self.dict_config)
