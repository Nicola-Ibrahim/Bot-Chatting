"""Authentication Service."""

from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Mapping

from ...domain.account.account import Account
from ...domain.account.value_objects.email import Email
from ...domain.interfaces.account_repository import AccountRepository
from ...domain.interfaces.session_repository import SessionRepository
from ...domain.session.session import Session
from ...domain.session.value_objects.refresh_token import RefreshToken
from ...domain.session.value_objects.session_id import SessionId
from ..interfaces.password_hasher import IPasswordHasher
from .issue_token_command import IssueTokenCommand
from .issue_token_dto import IssuedTokenDTO
from .login_command import LoginCommand
from .login_dto import LoginResultDTO
from .logout_command import LogoutCommand

TokenFactory = Callable[[Mapping[str, Any], timedelta | None], str]


class AuthenticationService:
    def __init__(
        self,
        account_repository: AccountRepository,
        session_repository: SessionRepository,
        password_hasher: IPasswordHasher,
        token_factory: TokenFactory,
        session_ttl: timedelta | None = None,
    ) -> None:
        self._accounts = account_repository
        self._sessions = session_repository
        self._hasher = password_hasher
        self._token_factory = token_factory
        self._session_ttl = session_ttl or timedelta(hours=12)

    def login(self, command: LoginCommand) -> tuple[Account, LoginResultDTO]:
        email = Email.create(command.email)
        account = self._accounts.get_by_email(str(email))
        if not account or not self._hasher.verify(command.password, account.hashed_password.value):
            raise ValueError("Invalid credentials")
        if not account.is_verified:
            raise ValueError("Account not verified")
        if not account.is_active:
            raise ValueError("Account inactive")

        refresh_value = secrets.token_urlsafe(48)
        refresh_token = RefreshToken.create(refresh_value)
        expires_at = datetime.now(timezone.utc) + self._session_ttl
        session = Session.issue(account_id=account.id, refresh_token=refresh_token, expires_at=expires_at)
        self._sessions.add(session)
        dto = LoginResultDTO(
            account_id=str(account.id.value),
            email=str(account.email),
            session_id=str(session.id.value),
            refresh_token=refresh_token.value,
        )
        return account, dto

    def logout(self, command: LogoutCommand) -> None:
        try:
            session_id = SessionId.create(uuid.UUID(command.session_id))
        except (ValueError, AttributeError) as exc:  # invalid UUID
            raise ValueError("Invalid session identifier") from exc
        session = self._sessions.get_by_id(session_id)
        if not session:
            return
        session.revoke()
        self._sessions.update(session)

    def issue_token(self, command: IssueTokenCommand) -> IssuedTokenDTO:
        claims: dict[str, Any] = {"sub": command.account_id}
        if command.session_id:
            claims["sid"] = command.session_id
        if command.extra_claims:
            claims.update(command.extra_claims)
        expires_delta = None
        if command.expires_in_seconds:
            expires_delta = timedelta(seconds=command.expires_in_seconds)
        token = self._token_factory(claims, expires_delta)
        return IssuedTokenDTO(access_token=token)
