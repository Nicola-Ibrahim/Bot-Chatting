from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .exception import BusinessRuleValidationException
from .rule import BaseBusinessRule


@dataclass(frozen=True)
class ValueObject(ABC):
    """Abstract base class for value objects."""

    def __eq__(self, other: Any) -> bool:
        """Check equality based on the value object properties."""
        if not isinstance(other, ValueObject):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Return the hash of the value object."""
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self) -> str:
        """Return the string representation of the value object."""
        return str(self.__dict__)

    def check_rules(self, *rule: BaseBusinessRule) -> None:
        """Check a business rule."""
        for rule in rule:
            if not rule.is_satisfied():
                raise BusinessRuleValidationException(rule)

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "ValueObject":
        """Abstract method for creating the value object, enforcing rule validation."""
        raise NotImplementedError
