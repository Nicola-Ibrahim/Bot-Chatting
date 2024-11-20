import logging
import os
from logging.handlers import TimedRotatingFileHandler

from colorama import Fore, Style, init

from ..config import LOG_DIR

# Initialize colorama for cross-platform support (especially on Windows)
init(autoreset=True)


class BaseLogger:
    """Base class for loggers with common functionality."""

    LOG_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def __init__(self, logger_name: str, level: int = logging.DEBUG):
        """Initialize the base logger."""
        self.logger_name = logger_name
        self.level = level
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.level)
        self.logger.addHandler(self._get_console_handler())

    def _get_console_handler(self) -> logging.StreamHandler:
        """Return a StreamHandler for logging to the console."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self._get_console_formatter())  # Use colored formatter for console
        return console_handler

    def _get_console_formatter(self) -> logging.Formatter:
        """Return a colorized formatter for console log messages."""
        return logging.Formatter(self._get_color_format())

    def _get_file_formatter(self) -> logging.Formatter:
        """Return a plain formatter for file log messages."""
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def _get_color_format(self) -> str:
        """Return a log format with color based on log level."""
        return "%(asctime)s - %(name)s - %(levelname_color)s - %(message)s"

    def __getattr__(self, name):
        """Delegate attribute access to the underlying logger."""
        return getattr(self.logger, name)


class ColoredFormatter(logging.Formatter):
    """Formatter that adds color to the log level name."""

    def format(self, record):
        log_color = BaseLogger.LOG_COLORS.get(record.levelno, Fore.WHITE)
        record.levelname_color = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class ConsoleLogger(BaseLogger):
    """Logger that handles logging to the console."""

    def _get_console_formatter(self) -> logging.Formatter:
        """Override to use the colored formatter."""
        return ColoredFormatter(self._get_color_format())


class FileLogger(BaseLogger):
    """Logger that handles logging to a file with rotation."""

    def __init__(self, logger_name: str, log_filename: str, level: int = logging.DEBUG):
        """Initialize the file logger."""
        super().__init__(logger_name, level)
        self.log_filename = log_filename
        self.logger.removeHandler(self.logger.handlers[0])  # Remove console handler
        self.logger.addHandler(self._get_file_handler())

    def _get_file_handler(self) -> TimedRotatingFileHandler:
        """Return a TimedRotatingFileHandler for logging to a rotating file."""
        log_file_path = self._ensure_log_file_exists()
        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when="midnight",
            interval=1,
            encoding="utf-8",
            backupCount=30,
        )
        file_handler.suffix = "%Y-%m-%d.log"
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self._get_file_formatter())  # Plain formatter for file
        return file_handler

    def _ensure_log_file_exists(self) -> str:
        """Ensure that the log directory and file exist."""
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file_path = os.path.join(LOG_DIR, self.log_filename + ".log")
        if not os.path.exists(log_file_path):
            open(log_file_path, "w").close()
        return log_file_path
