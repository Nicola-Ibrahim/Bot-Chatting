"""Command to mark an account as verified."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class VerifyAccountCommand:
    account_id: str
