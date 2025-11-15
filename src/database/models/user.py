from sqlalchemy import Boolean, Column, String

from .base import BaseSQLModel


class User(BaseSQLModel):
    __tablename__ = "users"

    # Store the domain identifier as a string UUID. This ensures
    # deterministic mapping between the domain aggregate and the
    # persistence layer. The column is unique and non‑null to prevent
    # duplicates and allow efficient lookups.
    uuid = Column(String(36), unique=True, nullable=False, index=True)

    # A unique email address for the user
    email = Column(String(320), unique=True, nullable=False, index=True)
    # The hashed password (e.g. SHA256, bcrypt etc.)
    hashed_password = Column(String(256), nullable=False)
    # Whether the user has completed email verification
    is_verified = Column(Boolean, nullable=False, default=False)
    # Whether the user account is active
    is_active = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<User(id={self.id}, uuid={self.uuid}, email={self.email}, "
            f"verified={self.is_verified}, active={self.is_active})>"
        )
