from ..conf.connector import DatabaseConnector


class PostgreSQLConnector(DatabaseConnector):
    """Connector for PostgreSQL databases."""

    def _get_connection_string(self) -> str:
        """Construct a connection string for PostgreSQL."""
        if self.connection_string:
            return self.connection_string
        if self.config:
            user = self.config.get("user", "")
            password = self._get_secret() or self.config.get("password", "")
            host = self.config.get("host", "localhost")
            port = self.config.get("port", "5432")
            database = self.config.get("database", "")
            return f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return None

    def _get_secret(self) -> str:
        """Retrieve the password if secret management is required."""
        if "vault_url" in self.config and "secret_name" in self.config:
            return self.get_secret(self.config["secret_name"], self.config["vault_url"])
        return None

    def get_secret(self, secret_name: str, vault_url: str) -> str:
        """Retrieve a secret from an external vault (e.g., Azure Key Vault)."""
        # Placeholder for secret retrieval (Azure, AWS, etc.)
        return "secret_value_from_vault"

    @classmethod
    def can_handle_connection_string(cls, connection_string: str, config: dict = None) -> bool:
        """Check if the connector can handle the connection string."""
        return connection_string.startswith("postgresql://")
