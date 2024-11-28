import logging
from abc import ABC, abstractmethod
from logging.handlers import TimedRotatingFileHandler

from colorama import Fore, Style, init

# Initialize colorama for cross-platform support (especially on Windows)
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formatter that adds color to log level names."""

    def __init__(self, fmt: str, log_colors: dict):
        super().__init__(fmt)
        self.log_colors = log_colors

    def format(self, record):
        log_color = self.log_colors.get(record.levelno, Fore.WHITE)
        record.levelname_color = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class BaseLogger(logging.Logger, ABC):

    def __init__(self, logger_name: str, config: dict):
        """Initialize the console logger with a name and configuration."""
        super().__init__(logger_name)
        self.config = config
        self._configure_logger()

    @abstractmethod
    def _configure_logger(self):
        pass


class ConsoleLogger(BaseLogger):
    """Logger specifically configured for console output."""

    def _configure_logger(self):
        """Configure the console handler."""

        # Set up the console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.config["level"])  # Use the level from config
        console_handler.setFormatter(ColoredFormatter(self.config["format"], self.config["log_colors"]))
        self.addHandler(console_handler)
        self.setLevel(self.config["level"])


class FileLogger(BaseLogger):
    """Logger specifically configured for file output."""

    def _configure_logger(self):
        """Configure the rotating file handler."""

        # Set up the rotating file handler
        log_file_path = self.config["log_file_path"]
        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when=self.config["when"],
            interval=self.config["interval"],
            encoding=self.config["encoding"],
            backupCount=self.config["backup_count"],
        )
        file_handler.setLevel(self.config["level"])
        file_handler.setFormatter(logging.Formatter(self.config["format"]))
        self.addHandler(file_handler)
        self.setLevel(self.config["level"])
        self.setLevel(self.config["level"])
        self.setLevel(self.config["level"])
        self.setLevel(self.config["level"])
