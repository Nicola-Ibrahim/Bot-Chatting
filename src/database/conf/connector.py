from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.engine import Engine, create_engine


class DatabaseConnector(ABC):
    """Abstract base class for database connectors."""

    def __init__(self, connection_string: Optional[str] = None, config: Optional[dict[str, str]] = None, **kwargs):
        """
        Initialize the database connector.

        Args:
            connection_string (Optional[str]): The connection string for the database.
            config (Optional[dict[str, str]]): Configuration dictionary with keys like 'user', 'password', 'host', 'port', 'database' for PostgreSQL or 'path' for SQLite.
            **kwargs: Additional arguments for the database engine.
        """
        if not connection_string and not config:
            raise ValueError("Either connection_string or config must be provided")
        self.connection_string = connection_string
        self.config = config
        self.kwargs = kwargs

    @abstractmethod
    def _get_connection_string(self) -> Optional[str]:
        """Construct the connection string."""
        pass

    def create_engine(self) -> Engine:
        """
        Create a SQLAlchemy engine.

        Returns:
            Engine: A SQLAlchemy engine instance.
        """
        connection_string = self._get_connection_string()
        if not connection_string:
            raise ValueError("Unable to determine connection string")
        return create_engine(connection_string, **self.kwargs)
