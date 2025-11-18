"""Handler that removes an account."""

from __future__ import annotations

import uuid

from src.modules.accounts.domain.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository

from .command import RemoveAccountCommand


class RemoveAccountHandler:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._accounts = account_repository

    def __call__(self, command: RemoveAccountCommand) -> None:
        try:
            account_id = AccountId.create(uuid.UUID(command.account_id))
        except (ValueError, AttributeError) as exc:
            raise ValueError("Invalid account identifier") from exc
        self._accounts.remove(account_id)
