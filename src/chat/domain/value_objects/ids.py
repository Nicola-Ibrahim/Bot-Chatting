import abc
import uuid
from dataclasses import dataclass

from .value_object import ValueObject


# Abstract Base Class for ID
class ID(ValueObject):
    """
    Abstract base class for any type of ID.
    It ensures consistency across different ID types.
    """

    @abc.abstractmethod
    def __eq__(self, other: "ID") -> bool:
        """Equality check based on ID value."""

    @abc.abstractmethod
    def __hash__(self) -> int:
        """Hash the ID."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        """String representation of the ID."""


# Concrete implementations of ID
@dataclass(frozen=True)
class UUIDID(ID):
    """Concrete implementation of ID for UUIDs."""

    value: uuid.UUID

    @classmethod
    def create(cls):
        cls(value=uuid.uuid4())

    def __eq__(self, other: ID) -> bool:
        return isinstance(other, UUIDID) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"UUIDID({self.value})"


@dataclass(frozen=True)
class IntID(ID):
    """Concrete implementation of ID for integers."""

    value: int

    def __eq__(self, other: ID) -> bool:
        return isinstance(other, IntID) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"IntID({self.value})"


@dataclass(frozen=True)
class StringID(ID):
    """Concrete implementation of ID for strings."""

    value: str

    def __eq__(self, other: ID) -> bool:
        return isinstance(other, StringID) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f"StringID({self.value})"
