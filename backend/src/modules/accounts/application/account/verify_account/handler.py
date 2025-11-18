"""Handler that verifies an account."""

from __future__ import annotations

import uuid

from src.modules.accounts.application.account.dto import AccountDTO, to_account_dto
from src.modules.accounts.domain.account.account import Account
from src.modules.accounts.domain.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository

from .command import VerifyAccountCommand


class VerifyAccountHandler:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._accounts = account_repository

    def __call__(self, command: VerifyAccountCommand) -> tuple[Account, AccountDTO]:
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
