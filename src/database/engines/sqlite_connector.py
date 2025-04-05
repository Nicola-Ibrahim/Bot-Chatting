from typing import Optional

from ..conf.connector import DatabaseConnector


class SQLiteConnector(DatabaseConnector):
    """Connector for SQLite databases."""

    def _get_connection_string(self) -> Optional[str]:
        """Construct a connection string for SQLite."""
        if self.connection_string:
            return self.connection_string
        if self.config and "path" in self.config:
            return f"sqlite:///{self.config['path']}"
        return None

    @classmethod
    def can_handle_connection_string(cls, connection_string: str, config: Optional[Dict[str, str]] = None) -> bool:
        """Check if the connector can handle the connection string."""
        return connection_string.startswith("sqlite://")
