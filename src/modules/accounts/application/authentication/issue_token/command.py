"""Command encapsulating the data for issuing an access token."""

from dataclasses import dataclass, field
from typing import Mapping, Any


@dataclass(slots=True, frozen=True)
class IssueTokenCommand:
    account_id: str
    session_id: str | None = None
    expires_in_seconds: int | None = None
    extra_claims: Mapping[str, Any] = field(default_factory=dict)
