"""Handler that updates mutable account fields."""

from __future__ import annotations

import uuid

from src.modules.accounts.application.account.dto import AccountDTO, to_account_dto
from src.modules.accounts.application.interfaces.password_hasher import IPasswordHasher
from src.modules.accounts.domain.account.account import Account
from src.modules.accounts.domain.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.account.value_objects.email import Email
from src.modules.accounts.domain.account.value_objects.hashed_password import HashedPassword
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository

from .command import UpdateAccountCommand


class UpdateAccountHandler:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self._accounts = account_repository
        self._hasher = password_hasher

    def __call__(self, command: UpdateAccountCommand) -> tuple[Account, AccountDTO]:
        try:
            account_id = AccountId.create(uuid.UUID(command.account_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError("Invalid account identifier") from exc

        account = self._accounts.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        if command.email:
            account.change_email(Email.create(command.email))
        if command.password:
            hashed = HashedPassword.create(self._hasher.encode(command.password))
            account.change_password(hashed)
        if command.is_active is True:
            account.activate()
        elif command.is_active is False:
            account.deactivate()

        self._accounts.update(account)
        dto = to_account_dto(account)
        return account, dto
