"""Application service orchestrating account use-cases."""

from __future__ import annotations

import uuid
from typing import Iterable, Optional, Tuple

from src.modules.accounts.application.access_control.assign_role.command import AssignRoleCommand
from src.modules.accounts.application.access_control.assign_role.handler import AssignRoleHandler
from src.modules.accounts.application.authentication.login.command import LoginCommand
from src.modules.accounts.application.authentication.login.dto import LoginResultDTO
from src.modules.accounts.application.authentication.login.handler import LoginHandler
from src.modules.accounts.application.authentication.logout.command import LogoutCommand
from src.modules.accounts.application.authentication.logout.handler import LogoutHandler
from src.modules.accounts.application.registration.register_account.command import RegisterAccountCommand
from src.modules.accounts.application.registration.register_account.handler import RegisterAccountHandler
from src.modules.accounts.domain.aggregates.account.account import Account
from src.modules.accounts.domain.aggregates.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.aggregates.account.value_objects.email import Email
from src.modules.accounts.domain.aggregates.account.value_objects.hashed_password import HashedPassword
from src.modules.accounts.domain.interfaces import AccountRepository, RoleRepository, SessionRepository

from ..interfaces.notification_service import INotificationService
from ..interfaces.password_hasher import IPasswordHasher


class AccountsService:
    """High-level façade over the accounts application layer."""

    def __init__(
        self,
        account_repository: AccountRepository,
        session_repository: SessionRepository,
        password_hasher: IPasswordHasher,
        notification_service: INotificationService,
        role_repository: RoleRepository | None = None,
    ) -> None:
        self._accounts = account_repository
        self._sessions = session_repository
        self._hasher = password_hasher
        self._notifications = notification_service
        self._roles = role_repository

        self._register_handler = RegisterAccountHandler(account_repository, password_hasher, notification_service)
        self._login_handler = LoginHandler(account_repository, session_repository, password_hasher)
        self._logout_handler = LogoutHandler(session_repository)
        self._assign_role_handler = AssignRoleHandler(account_repository, role_repository) if role_repository else None

    # ------------------------------------------------------------------
    # Registration & verification
    # ------------------------------------------------------------------
    def register_user(self, email: str, password: str) -> Account:
        account, _ = self._register_handler(RegisterAccountCommand(email=email, password=password))
        return account

    def verify_user(self, account_id: str) -> Account:
        account = self._get_account_or_raise(account_id)
        account.verify()
        self._accounts.update(account)
        return account

    # ------------------------------------------------------------------
    # Authentication & sessions
    # ------------------------------------------------------------------
    def authenticate(self, email: str, password: str) -> Tuple[Account, LoginResultDTO]:
        account, dto = self._login_handler(LoginCommand(email=email, password=password))
        return account, dto

    def logout(self, session_id: str) -> None:
        self._logout_handler(LogoutCommand(session_id=session_id))

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get_user(self, account_id: str) -> Optional[Account]:
        account_id_vo = self._parse_account_id(account_id)
        return self._accounts.get_by_id(account_id_vo)

    def list_users(self) -> Iterable[Account]:
        return self._accounts.list_accounts()

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------
    def update_user(
        self,
        account_id: str,
        *,
        email: str | None = None,
        password: str | None = None,
        is_active: bool | None = None,
    ) -> Account:
        account = self._get_account_or_raise(account_id)
        if email:
            account.change_email(Email.create(email))
        if password:
            hashed = HashedPassword.create(self._hasher.encode(password))
            account.change_password(hashed)
        if is_active is True:
            account.activate()
        elif is_active is False:
            account.deactivate()
        self._accounts.update(account)
        return account

    def remove_user(self, account_id: str) -> None:
        account = self._get_account_or_raise(account_id)
        self._accounts.remove(account.id)

    def assign_role(self, account_id: str, role_id: str) -> None:
        if not self._assign_role_handler:
            raise RuntimeError("Role repository not configured")
        self._assign_role_handler(AssignRoleCommand(account_id=account_id, role_id=role_id))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_account_or_raise(self, account_id: str) -> Account:
        account = self.get_user(account_id)
        if not account:
            raise ValueError("Account not found")
        return account

    def _parse_account_id(self, account_id: str) -> AccountId:
        try:
            return AccountId(uuid.UUID(account_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError("Invalid account identifier") from exc
