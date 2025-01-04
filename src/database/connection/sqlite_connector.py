import os
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from .connector import DatabaseConnector


@dataclass
class SQLiteConnector(DatabaseConnector):
    """Connector for SQLite databases."""

    def create_engine(self) -> Engine:
        """
        Create an SQLite engine dynamically.

        Args:
            database_path (str): Path to the SQLite database file.
            config (dict): Configuration dictionary with key 'path'.
            **kwargs: Additional arguments for SQLAlchemy's `create_engine`.

        Returns:
            Engine: A SQLAlchemy engine instance.
        """
        if self.connection_string:
            connection_string = self.connection_string
        elif self.config and "path" in self.config:
            # Get the database path from config dictionary
            connection_string = self._get_connection_string_from_path(self.config["path"])
        else:
            # Fallback to environment variables
            connection_string = self._get_connection_string_from_env()

        if not connection_string:
            raise ValueError("Unable to determine connection string for SQLite")

        return create_engine(connection_string, **self.kwargs)

    def _get_connection_string_from_path(database_path: str) -> str:
        """Construct a connection string from a database path."""
        return f"sqlite:///{database_path}"

    def _get_connection_string_from_env() -> str:
        """Construct a connection string from environment variables."""
        database_path = os.getenv("DB_SQLITE_PATH", "")
        if database_path:
            return f"sqlite:///{database_path}"
        return ""
