"""Command to delete an account."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RemoveAccountCommand:
    account_id: str
