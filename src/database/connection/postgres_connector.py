import os
from dataclasses import dataclass

from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from .connector import DatabaseConnector


@dataclass
class PostgreSQLConnector(DatabaseConnector):
    """Connector for PostgreSQL databases."""

    def create_engine(self) -> Engine:
        """
        Create a PostgreSQL engine dynamically.

        Args:
            connection_string (str): Direct PostgreSQL connection string.
            config (dict): Configuration dictionary with keys like user, password, host, port, database.
            **kwargs: Additional arguments for SQLAlchemy's `create_engine`.

        Returns:
            Engine: A SQLAlchemy engine instance.
        """
        if self.connection_string:
            # Use the provided connection string directly
            return create_engine(self.connection_string, **self.kwargs)
        elif self.config:
            # Construct the connection string from a config dictionary
            connection_string = self._get_connection_string_from_config(self.config)
        else:
            # Fallback to environment variables
            connection_string = self._get_connection_string_from_env()

        if not connection_string:
            raise ValueError("Unable to determine connection string for PostgreSQL")

        return create_engine(connection_string, **self.kwargs)

    def _get_connection_string_from_config(self, config: dict[str, str]) -> str:
        """Construct a connection string from a configuration dictionary."""
        user = config.get("user", "")
        password = config.get("password", "")
        host = config.get("host", "localhost")
        port = config.get("port", "5432")
        database = config.get("database", "")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def _get_connection_string_from_env(self) -> str:
        """Construct a connection string from environment variables."""
        user = os.getenv("DB_USER", "")
        password = os.getenv("DB_PASSWORD", "")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_DATABASE", "")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
