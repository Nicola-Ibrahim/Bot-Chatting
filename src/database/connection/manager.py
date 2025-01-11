import re
from typing import Optional, Type

from sqlalchemy.engine import Engine

from .aws_connector import AWSConnector
from .azure_connector import AzureConnector
from .connector import DatabaseConnector
from .postgres_connector import PostgreSQLConnector
from .sqlite_connector import SQLiteConnector


class DatabaseConnectionManager:
    """Manager for dynamically creating database connections."""

    CONNECTOR_CLASSES: dict[str, Type[DatabaseConnector]] = {
        "postgresql": PostgreSQLConnector,
        "sqlite": SQLiteConnector,
        "aws": AWSConnector,
        "azure": AzureConnector,
    }

    @staticmethod
    def create_db_engine(
        connection_string: Optional[str] = None,
        config: Optional[dict[str, str]] = None,
        **kwargs,
    ) -> Engine:
        """
        Create a database engine dynamically based on the connection string or config.

        Args:
            connection_string (Optional[str]): The connection string for the database.
            config (Optional[dict]): Configuration dictionary with keys like 'user', 'password', 'host', 'port', 'database' for PostgreSQL or 'path' for SQLite.
            **kwargs: Additional arguments for the database engine.

        Returns:
            Engine: SQLAlchemy Engine instance.

        Raises:
            ValueError: If the connection string or config is invalid.
            TypeError: If neither a connection string nor config is provided.
        """
        connector = DatabaseConnectionManager._get_connector(connection_string, config, **kwargs)
        return connector.create_engine()

    @staticmethod
    def _get_connector(
        connection_string: Optional[str], config: Optional[dict[str, str]], **kwargs
    ) -> DatabaseConnector:
        """
        Get the appropriate connector based on the connection string or config.

        Args:
            connection_string (Optional[str]): The connection string for the database.
            config (Optional[dict]): Configuration dictionary.

        Returns:
            DatabaseConnector: The appropriate connector instance.

        Raises:
            ValueError: If the connection string or config is invalid.
        """
        if connection_string:
            driver = DatabaseConnectionManager._detect_driver_from_connection_string(connection_string)
        elif config:
            driver = config.get("cloud", "postgresql")
        else:
            raise TypeError("Either connection_string or config must be provided")

        connector_class = DatabaseConnectionManager.CONNECTOR_CLASSES.get(driver)
        if not connector_class:
            raise ValueError(f"Unsupported driver: {driver}")

        return connector_class(connection_string=connection_string, config=config, kwargs=kwargs)

    @staticmethod
    def _detect_driver_from_connection_string(connection_string: str) -> str:
        """
        Detect the database type from the connection string.

        Args:
            connection_string (str): The database connection string.

        Returns:
            str: The detected database driver (e.g., 'postgresql', 'sqlite').
        """
        if re.match(r"^postgresql://", connection_string):
            return "postgresql"
        elif re.match(r"^sqlite://", connection_string):
            return "sqlite"
        else:
            raise ValueError(f"Unsupported connection string format: {connection_string}")

    @staticmethod
    def test_connection(engine: Engine) -> bool:
        """
        Test the database connection.

        Args:
            engine (Engine): SQLAlchemy Engine instance.

        Returns:
            bool: True if the connection succeeds.

        Raises:
            ConnectionError: If the connection test fails.
        """
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except Exception as e:
            raise ConnectionError(f"Database connection test failed: {e}") from e
