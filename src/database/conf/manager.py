from typing import Type

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from .connector import DatabaseConnector


class DatabaseConnectionManager:
    """Manages database connections using dependency injection."""

    def __init__(
        self,
        connector_class: Type[DatabaseConnector],
        connection_string: str | None = None,
        config: dict[str, str] | None = None,
        **kwargs,
    ):
        """
        Initialize the manager with a connector class, connection string, or config.
        """
        self.connector = connector_class(connection_string=connection_string, config=config, **kwargs)
        self._engine: Engine = self.connector.create_engine()

    @property
    def session(self):
        """
        Create a new session for database operations.

        Returns:
            Session: A new SQLAlchemy session.
        """
        with sessionmaker(bind=self._engine)() as session:
            yield session

    def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns:
            bool: True if the connection is successful, otherwise raises an error.
        """
        try:
            with self._engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}") from e
