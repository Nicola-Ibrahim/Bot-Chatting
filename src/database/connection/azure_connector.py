from dataclasses import dataclass, field
from typing import Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from .connector import DatabaseConnector


@dataclass
class AzureConnector(DatabaseConnector):
    """Azure Connector for various database types, supporting Azure Key Vault integration.

    Example Usage:

    Creating a Connection with Config:
    ```python
    config_dict = {
        "user": "your_db_user",
        "password": "your_db_password",  # This can be fetched from Key Vault
        "host": "your_db_host",
        "port": 5432,
        "database": "your_database_name",
        "db_type": "postgresql",
        "vault_url": "https://your-vault-name.vault.azure.net/",
        "secret_name": "your-secret-name",
    }

    azure_connector = AzureConnector(
        config=config_dict
    )
    engine = azure_connector.create_engine()
    ```

    Creating a Connection with Connection String:
    ```python
    connection_string = "postgresql://user:password@your_db_host:5432/your_database_name"
    azure_connector = AzureConnector(
        connection_string=connection_string
    )
    engine = azure_connector.create_engine()
    ```
    """

    connection_string: Optional[str] = None
    config: Optional[Dict[str, str]] = None
    kwargs: Dict = field(default_factory=dict)

    def create_engine(self) -> Engine:
        """
        Create a SQLAlchemy Engine for connecting to the Azure database.

        - If a connection string is provided, use it directly.
        - If a config is provided, construct the connection string, optionally using Azure Key Vault for secrets.

        Returns:
            Engine: SQLAlchemy Engine instance.

        Raises:
            ValueError: If neither a connection string nor config is provided.
        """
        if self.connection_string:
            return create_engine(self.connection_string, **self.kwargs)

        elif self.config:
            # Extract connection details from the config
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
        # Create a credential using DefaultAzureCredential for Azure SDK
        credential = DefaultAzureCredential()

        # Instantiate the Key Vault SecretClient
        client = SecretClient(vault_url=vault_url, credential=credential)

        # Fetch the secret from the specified Azure Key Vault
        secret = client.get_secret(secret_name)

        # Return the secret value
        return secret.value
