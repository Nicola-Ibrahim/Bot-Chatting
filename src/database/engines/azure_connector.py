from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .connector import DatabaseConnector


class AzureConnector(DatabaseConnector):
    """Azure Connector for various database types, supporting Azure Key Vault integration."""

    def create_engine(self) -> Engine:
        """
        Create a SQLAlchemy Engine for connecting to the Azure database.
        """
        if self.connection_string:
            return create_engine(self.connection_string, **self.kwargs)

        elif self.config:
            # Retrieve password from Azure Key Vault if needed
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host")
            port = self.config.get("port", 5432)  # Default PostgreSQL port
            database = self.config.get("database")
            db_type = self.config.get("db_type", "postgresql")

            # Retrieve the password from Azure Key Vault if needed
            if "vault_url" in self.config and "secret_name" in self.config:
                password = self.get_secret(self.config["secret_name"], self.config["vault_url"])

            # Construct the connection string
            connection_string = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
            return create_engine(connection_string, **self.kwargs)

        else:
            raise ValueError("Either connection_string or config must be provided")

    def get_secret(self, secret_name: str, vault_url: str) -> str:
        """Retrieve a secret from Azure Key Vault."""
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value

    @classmethod
    def can_handle_connection_string(cls, connection_string: str, config: Optional[dict] = None) -> bool:
        """Check if the connector can handle the connection string."""
        return connection_string.startswith("postgresql://") or connection_string.startswith("mysql://")
