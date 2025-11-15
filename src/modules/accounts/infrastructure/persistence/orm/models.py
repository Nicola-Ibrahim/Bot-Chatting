"""SQLAlchemy models for the accounts bounded context."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import relationship

from src.database.models.base import Base, BaseModel  # type: ignore

# Association table linking accounts and roles.
account_roles = Table(
    "account_roles",
    Base.metadata,
    Column("account_id", ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class AccountModel(BaseModel):  # type: ignore[misc]
    __tablename__ = "accounts"

    uuid = Column(String(36), unique=True, nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)

    credential = relationship(
        "CredentialModel",
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan",
    )
    sessions = relationship("SessionModel", back_populates="account", cascade="all, delete-orphan")
    roles = relationship("RoleModel", secondary=account_roles, back_populates="accounts")


class CredentialModel(BaseModel):  # type: ignore[misc]
    __tablename__ = "account_credentials"

    account_id = Column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, unique=True)
    hashed_password = Column(String(512), nullable=False)

    account = relationship("AccountModel", back_populates="credential")


class SessionModel(BaseModel):  # type: ignore[misc]
    __tablename__ = "sessions"

    session_uuid = Column(String(36), unique=True, nullable=False, index=True)
    account_id = Column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    refresh_token = Column(String(512), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    account = relationship("AccountModel", back_populates="sessions")


class RoleModel(BaseModel):  # type: ignore[misc]
    __tablename__ = "roles"

    uuid = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    accounts = relationship("AccountModel", secondary=account_roles, back_populates="roles")
