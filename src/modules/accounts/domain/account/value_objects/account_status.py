"""Value object encapsulating account lifecycle flags."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class AccountStatus(ValueObject):
    is_verified: bool = False
    is_active: bool = True

    @classmethod
    def create(cls, *, is_verified: bool = False, is_active: bool = True) -> Self:
        return cls(is_verified=is_verified, is_active=is_active)

    def mark_verified(self) -> "AccountStatus":
        return AccountStatus(is_verified=True, is_active=self.is_active)

    def activate(self) -> "AccountStatus":
        return AccountStatus(is_verified=self.is_verified, is_active=True)

    def deactivate(self) -> "AccountStatus":
        return AccountStatus(is_verified=self.is_verified, is_active=False)
