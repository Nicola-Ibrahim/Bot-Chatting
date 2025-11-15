"""Plaintext password value object used for validation before hashing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from src.building_blocks.domain.value_object import ValueObject

from ..rules.password_must_meet_policy_rule import PasswordMustMeetPolicyRule


@dataclass(frozen=True, slots=True)
class Password(ValueObject):
    value: str

    @classmethod
    def create(cls, value: str) -> Self:
        cls.check_rules(PasswordMustMeetPolicyRule(password=value))
        return cls(value=value)

    def masked(self) -> str:
        """Return a masked representation for logging/debugging."""
        return "*" * min(len(self.value), 4)
