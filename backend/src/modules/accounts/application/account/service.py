"""Account Service."""

from __future__ import annotations

import uuid
from typing import Optional

from ...domain.account.account import Account
from ...domain.account.value_objects.account_id import AccountId
from ...domain.account.value_objects.email import Email
from ...domain.account.value_objects.hashed_password import HashedPassword
from ...domain.interfaces.account_repository import AccountRepository
from ..interfaces.password_hasher import IPasswordHasher
from .dto import AccountDTO, to_account_dto
from .get_account_query import GetAccountQuery
from .list_accounts_query import ListAccountsQuery
from .remove_account_command import RemoveAccountCommand
from .update_account_command import UpdateAccountCommand
from .verify_account_command import VerifyAccountCommand


class AccountService:
    def __init__(
        self,
        account_repository: AccountRepository,
        password_hasher: IPasswordHasher,
    ) -> None:
        self._accounts = account_repository
        self._hasher = password_hasher

    def get(self, query: GetAccountQuery) -> Optional[AccountDTO]:
        try:
            account_id = AccountId.create(uuid.UUID(query.account_id))
        except (ValueError, AttributeError):
            return None
        account = self._accounts.get_by_id(account_id)
        if not account:
            return None
        return to_account_dto(account)

    def list(self, query: ListAccountsQuery) -> tuple[AccountDTO, ...]:
        accounts = (to_account_dto(account) for account in self._accounts.list_accounts())
        return tuple(accounts)

    def update(self, command: UpdateAccountCommand) -> tuple[Account, AccountDTO]:
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

    def remove(self, command: RemoveAccountCommand) -> None:
        try:
            account_id = AccountId.create(uuid.UUID(command.account_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError("Invalid account identifier") from exc
        self._accounts.remove(account_id)

    def verify(self, command: VerifyAccountCommand) -> tuple[Account, AccountDTO]:
        try:
            account_id = AccountId.create(uuid.UUID(command.account_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError("Invalid account identifier") from exc

        account = self._accounts.get_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        account.verify()
        self._accounts.update(account)
        dto = to_account_dto(account)
        return account, dto
