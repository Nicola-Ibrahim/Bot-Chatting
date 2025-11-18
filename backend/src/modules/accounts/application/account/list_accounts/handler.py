"""Query handler that lists all accounts."""

from __future__ import annotations

from src.modules.accounts.application.account.dto import AccountDTO, to_account_dto
from src.modules.accounts.domain.interfaces.account_repository import AccountRepository

from .query import ListAccountsQuery


class ListAccountsHandler:
    def __init__(self, account_repository: AccountRepository) -> None:
        self._accounts = account_repository

    def __call__(self, query: ListAccountsQuery) -> tuple[AccountDTO, ...]:
        accounts = (to_account_dto(account) for account in self._accounts.list_accounts())
        return tuple(accounts)
