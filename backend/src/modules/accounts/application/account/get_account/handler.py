"""Query handler that fetches an account by id."""

from __future__ import annotations

import uuid
from typing import Optional

from src.modules.accounts.application.account.dto import AccountDTO, to_account_dto
from src.modules.accounts.domain.account.value_objects.account_id import AccountId
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository

from .query import GetAccountQuery


class GetAccountHandler:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._accounts = account_repository

    def __call__(self, query: GetAccountQuery) -> Optional[AccountDTO]:
        try:
            account_id = AccountId.create(uuid.UUID(query.account_id))
        except (ValueError, AttributeError):
            return None
        account = self._accounts.get_by_id(account_id)
        if not account:
            return None
        return to_account_dto(account)
