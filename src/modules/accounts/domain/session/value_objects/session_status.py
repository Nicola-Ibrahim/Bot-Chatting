"""Value object describing the lifecycle of a session."""

from dataclasses import dataclass
from typing import Self

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class SessionStatus(ValueObject):
    is_active: bool = True

    @classmethod
    def active(cls) -> Self:
        return cls(is_active=True)

    @classmethod
    def revoked(cls) -> Self:
        return cls(is_active=False)

    def revoke(self) -> "SessionStatus":
        return SessionStatus(is_active=False)
