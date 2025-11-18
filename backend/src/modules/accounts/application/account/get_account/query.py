"""Query to fetch a single account."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetAccountQuery:
    account_id: str
