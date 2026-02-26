"""Registration Service."""

from __future__ import annotations

from ...domain.account.account import Account
from ...domain.account.value_objects.email import Email
from ...domain.account.value_objects.hashed_password import HashedPassword
from ...domain.account.value_objects.password import Password
from ...domain.interfaces.account_repository import AccountRepository
from ..interfaces.notification_service import INotificationService
from ..interfaces.password_hasher import IPasswordHasher
from .register_account_command import RegisterAccountCommand
from .register_account_dto import RegisteredAccountDTO


class RegistrationService:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_hasher: IPasswordHasher,
        notification_service: INotificationService,
    ) -> None:
        self._accounts = account_repository
        self._hasher = password_hasher
        self._notifications = notification_service

    def register(self, command: RegisterAccountCommand) -> tuple[Account, RegisteredAccountDTO]:
        email_vo = Email.create(command.email)
        password_vo = Password.create(command.password)
        if self._accounts.exists_by_email(str(email_vo)):
            raise ValueError("An account with this email already exists")
        hashed = HashedPassword.create(self._hasher.encode(password_vo.value))
        account = Account.register(email=email_vo, hashed_password=hashed)
        self._accounts.add(account)
        self._notifications.send_welcome_email(str(email_vo))
        dto = RegisteredAccountDTO(
            id=str(account.id.value),
            email=str(email_vo),
            is_verified=account.is_verified,
            is_active=account.is_active,
        )
        return account, dto
