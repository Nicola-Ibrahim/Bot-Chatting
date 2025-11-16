"""Command for revoking a session."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LogoutCommand:
    session_id: str
