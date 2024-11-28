import logging
import os
from typing import Any, Dict, List, Optional

from colorama import Fore, Style, init
from pydantic import BaseModel

# Initialize colorama for cross-platform support
init(autoreset=True)

LOG_DIR = "./logs"  # Default log directory


class LoggerConfig(BaseModel):
    """Root logger configuration."""

    level: str = "DEBUG"
    format: str = "%(asctime)s - %(name)s - %(levelname_color)s - %(message)s"
    log_colors: Optional[dict] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }
    log_to_console: bool = True  # Should log to the console
    log_to_file: bool = True  # Should log to a file
    log_filename: str = "application.log"
    log_dir: str = LOG_DIR
    when: str = "midnight"  # For rotating logs
    interval: int = 1
    backup_count: int = 30
    encoding: str = "utf-8"

    def log_file_path(self) -> str:
        """Ensure the log directory exists and return the full log file path."""
        os.makedirs(self.log_dir, exist_ok=True)
        return os.path.join(self.log_dir, self.log_filename)


class LoggerConfig(BaseModel):
    """Root logger configuration."""

    version: int = 1
    disable_existing_loggers: bool = False
    console: Optional[ConsoleConfig] = None
    file: Optional[FileConfig] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary compatible with logging.config.dictConfig."""
        handlers: Dict[str, Dict[str, Any]] = {}
        formatters: Dict[str, Dict[str, Any]] = {}
        root_handlers: List[str] = []

        if self.console:
            handlers["console"] = {
                "class": "logging.StreamHandler",
                "level": self.console.level,
                "formatter": "console_formatter",
                "stream": self.console.stream,
            }
            formatters["console_formatter"] = {"format": self.console.format}
            root_handlers.append("console")

        if self.file:
            handlers["file"] = {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": self.file.level,
                "formatter": "file_formatter",
                "filename": self.file.filename,
                "when": self.file.when,
                "interval": self.file.interval,
                "backupCount": self.file.backup_count,
                "encoding": self.file.encoding,
            }
            formatters["file_formatter"] = {"format": self.file.format}
            root_handlers.append("file")

        return {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "handlers": handlers,
            "formatters": formatters,
            "root": {
                "level": self.console.level if self.console else self.file.level,
                "handlers": root_handlers,
            },
        }


# Define a custom configuration for the chat application
chat_file_config = FileConfig(
    level="INFO",  # Only log INFO and above
    log_filename="chat_application.log",
    log_dir=str(Path.home() / "chat_logs"),  # Save logs in the user's home directory under 'chat_logs'
    when="midnight",  # Rotate logs daily
    interval=1,
    backup_count=7,  # Keep the last 7 logs
    encoding="utf-8",
)
