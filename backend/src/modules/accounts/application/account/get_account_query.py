"""Query to fetch a single account."""

from src.modules.accounts.application.contracts.query import BaseQuery


class GetAccountQuery(BaseQuery):
    account_id: str
