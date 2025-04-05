from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from .connector import DatabaseConnector


class AWSConnector(DatabaseConnector):
    """AWS Connector for various database types, integrating AWS Secrets Manager for secure password management."""

    def create_engine(self) -> Engine:
        """
        Create a SQLAlchemy Engine for connecting to the AWS database.
        """
        if self.connection_string:
            return create_engine(self.connection_string, **self.kwargs)

        elif self.config:
            user = self.config.get("user")
            password = self.config.get("password")
            host = self.config.get("host")
            port = self.config.get("port", 5432)
            database = self.config.get("database")
            db_type = self.config.get("db_type", "postgresql")

            if "secret_name" in self.config and "region_name" in self.config:
                password = self.get_secret(self.config["secret_name"], self.config["region_name"])

            connection_string = f"{db_type}://{user}:{password}@{host}:{port}/{database}"
            return create_engine(connection_string, **self.kwargs)

        else:
            raise ValueError("Either connection_string or config must be provided")

    def get_secret(self, secret_name: str, region_name: str) -> str:
        """Retrieve a secret from AWS Secrets Manager."""
        client = boto3.client("secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response["SecretString"]
            return secret
        except NoCredentialsError:
            raise ValueError("AWS credentials not found. Ensure your AWS credentials are configured.")
        except ClientError as e:
            raise ValueError(f"Error retrieving secret from AWS Secrets Manager: {e}")

    @classmethod
    def can_handle_connection_string(cls, connection_string: str, config: Optional[dict] = None) -> bool:
        """Check if the connector can handle the connection string."""
        return connection_string.startswith("postgresql://") or connection_string.startswith("mysql://")
