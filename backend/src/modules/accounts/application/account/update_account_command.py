"""Command to update account details."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class UpdateAccountCommand:
    account_id: str
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
