"""Command for logging an account into the system."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LoginCommand:
    email: str
    password: str
