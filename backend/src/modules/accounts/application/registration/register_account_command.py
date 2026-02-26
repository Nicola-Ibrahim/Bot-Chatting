"""Command object for registering a new account."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RegisterAccountCommand:
    email: str
    password: str
