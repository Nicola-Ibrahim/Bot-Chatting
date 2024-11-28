import logging

from .config import LoggerConfig


class ColoredFormatter(logging.Formatter):
    """Formatter that adds color to log level names."""

    def __init__(self, fmt: str, log_colors: dict):
        super().__init__(fmt)
        self.log_colors = log_colors

    def format(self, record):
        log_color = self.log_colors.get(record.levelno, Fore.WHITE)
        record.levelname_color = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


class ConversationLogger:
    """
    A unified logger for managing conversation logs. Can log to console, file, or both.
    """

    def __init__(self, config: LoggerConfig):
        """
        Initialize the logger with the provided configuration.
        The logger will be set up based on whether logging is enabled for console and/or file.
        """
        self.config = config
        self.logger = logging.getLogger("conversation_logger")
        self._configure_logger()

    def _configure_logger(self):
        """Configure the logger with console and file handlers based on the config."""
        handlers = []
        level = self.config.level.upper()

        # Console logging configuration
        if self.config.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(ColoredFormatter(self.config.format, self.config.log_colors))
            handlers.append(console_handler)

        # File logging configuration
        if self.config.log_to_file:
            file_handler = TimedRotatingFileHandler(
                filename=self.config.log_file_path(),
                when=self.config.when,
                interval=self.config.interval,
                backupCount=self.config.backup_count,
                encoding=self.config.encoding,
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(self.config.format))
            handlers.append(file_handler)

        # Add handlers to the logger
        self.logger.setLevel(level)
        for handler in handlers:
            self.logger.addHandler(handler)

    def log_message(self, user_id: str, conversation_id: str, message: str, level: int = logging.INFO, **extra):
        """
        Log a conversation message with user and conversation context.

        Args:
            user_id (str): The ID of the user.
            conversation_id (str): The ID of the conversation.
            message (str): The log message content.
            level (int): The log level (default: logging.INFO).
            **extra: Additional context (e.g., timestamps, IP address, etc.).
        """
        log_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message": message,
        }
        log_data.update(extra)

        log_message = f"Conversation {conversation_id} | User {user_id}: {message}"
        self._log(level, log_message, extra=log_data)

    def log_error(self, error: str, user_id: str = None, conversation_id: str = None, **extra):
        """
        Log an error related to conversations, with optional user and conversation context.

        Args:
            error (str): The error message.
            user_id (str, optional): The ID of the user, if applicable.
            conversation_id (str, optional): The ID of the conversation, if applicable.
            **extra: Additional context (e.g., error details, stack traces).
        """
        log_data = {
            "error": error,
            "user_id": user_id,
            "conversation_id": conversation_id,
        }
        log_data.update(extra)

        error_message = f"Conversation error: {error}"
        self._log(logging.ERROR, error_message, extra=log_data)

    def _log(self, level: int, message: str, extra: dict):
        """
        A helper method to log messages at different levels, while adding extra context.

        Args:
            level (int): The log level.
            message (str): The log message content.
            extra (dict): Additional context for the log message.
        """
        extra["levelname"] = logging.getLevelName(level)
        self.logger.log(level, message, extra=extra)

    def log_event(self, event_name: str, user_id: str, conversation_id: str, **extra):
        """
        Log a specific event related to the conversation. This allows for tracking events
        within a conversation (e.g., message sent, message read).

        Args:
            event_name (str): The name of the event (e.g., "message_sent").
            user_id (str): The ID of the user.
            conversation_id (str): The ID of the conversation.
            **extra: Additional context (e.g., message data, timestamps).
        """
        log_data = {
            "event_name": event_name,
            "user_id": user_id,
            "conversation_id": conversation_id,
        }
        log_data.update(extra)

        event_message = f"Event {event_name} for Conversation {conversation_id} | User {user_id}"
        self._log(logging.INFO, event_message, extra=log_data)
        self._log(logging.INFO, event_message, extra=log_data)
