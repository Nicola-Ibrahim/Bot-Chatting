import secrets
from datetime import datetime, timedelta, timezone

from src.modules.accounts.domain.account.account import Account
from src.modules.accounts.domain.account.value_objects.email import Email
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository
from src.modules.accounts.domain.interfaces.session_repository import SessionRepository
from src.modules.accounts.domain.session.session import Session
from src.modules.accounts.domain.session.value_objects.refresh_token import RefreshToken

from ...interfaces.password_hasher import IPasswordHasher
from .command import LoginCommand
from .dto import LoginResultDTO


class LoginHandler:
    def __init__(
        self,
        account_repository: AccountRepository,
        session_repository: SessionRepository,
        password_hasher: IPasswordHasher,
        session_ttl: timedelta | None = None,
    ) -> None:
        self._accounts = account_repository
        self._sessions = session_repository
        self._hasher = password_hasher
        self._session_ttl = session_ttl or timedelta(hours=12)

    def __call__(self, command: LoginCommand) -> tuple[Account, LoginResultDTO]:
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
