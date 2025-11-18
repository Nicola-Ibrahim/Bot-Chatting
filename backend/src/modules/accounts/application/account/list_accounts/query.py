"""Query to list accounts."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ListAccountsQuery:
    pass
