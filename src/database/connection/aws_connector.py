from dataclasses import dataclass, field
from typing import Dict, Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from .connector import DatabaseConnector


@dataclass
class AWSConnector(DatabaseConnector):
    """AWS Connector for various database types, integrating AWS Secrets Manager for secure password management.

    Example usage:
        Using connection string:
            connector = AWSConnector(connection_string="postgresql://user:password@host:5432/database")
            engine = connector.create_engine()

        Using config:
            config = {
                "user": "username",
                "password": "password",
                "host": "hostname",
                "port": 5432,
                "database": "dbname",
                "db_type": "postgresql",
                "secret_name": "my_secret",
                "region_name": "us-west-2"
            }
            connector = AWSConnector(config=config)
            engine = connector.create_engine()
    """

    connection_string: Optional[str] = None
    config: Optional[Dict[str, str]] = None
    kwargs: Dict = field(default_factory=dict)

    def create_engine(self) -> Engine:
        """
        Create a SQLAlchemy Engine for connecting to the AWS database.

        - If a connection string is provided, it is used directly.
        - If a config is provided, it constructs the connection string, optionally using AWS Secrets Manager for secrets.

        Returns:
            Engine: SQLAlchemy Engine instance.

        Raises:
            ValueError: If neither a connection string nor config is provided.
        """
        if self.connection_string:
            return create_engine(self.connection_string, **self.kwargs)

        elif self.config:
            # Extract database connection details from the config
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host")
            port = self.config.get("port", 5432)  # Default PostgreSQL port
            database = self.config.get("database")
            db_type = self.config.get("db_type", "postgresql")

            # If password is not provided in the config, retrieve it from AWS Secrets Manager
            if "secret_name" in self.config and "region_name" in self.config:
                secret = self.get_secret(self.config["secret_name"], self.config["region_name"])
                password = secret  # Update password with the value from Secrets Manager

            # Construct the connection string based on the database type
            connection_string = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
            return create_engine(connection_string, **self.kwargs)

        else:
            raise ValueError("Either connection_string or config must be provided")

    def get_secret(self, secret_name: str, region_name: str) -> str:
        """Retrieve a secret from AWS Secrets Manager."""
        # Create a Secrets Manager client using the specified region
        client = boto3.client("secretsmanager", region_name=region_name)

        try:
            # Fetch the secret from AWS Secrets Manager
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            # Extract and return the secret value (assumes the secret is stored as a string)
            secret = get_secret_value_response["SecretString"]
            return secret
        except NoCredentialsError:
            raise ValueError("AWS credentials not found. Ensure your AWS credentials are configured.")
        except ClientError as e:
            raise ValueError(f"Error retrieving secret from AWS Secrets Manager: {e}")
