import abc
import uuid
from dataclasses import dataclass, field

from .value_object import ValueObject


class ID:
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
class UUID4ID(ID):
    """Concrete implementation of ID for UUIDs."""

    value: uuid.UUID

    @classmethod
    def create(cls):
        return cls(value=uuid.uuid4())

    def __eq__(self, other: ID) -> bool:
        return isinstance(other, UUID4ID) and self.value == other.value

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


@dataclass(frozen=True)
class Identifier(ValueObject):
    value: ID = field(default_factory=UUID4ID.create())

    def validate(self) -> bool:
        """
        Validates the value of the identifier based on its type.

        Returns:
            ID: The validated ID object.

        Raises:
            ValueError: If the value is not valid for the given ID type.
            TypeError: If the value type is unsupported.
        """
        if isinstance(self.value, UUID4ID):
            if not isinstance(self.value.value, uuid.UUID):
                raise ValueError(f"Invalid UUID value provided: {self.value.value}")
        elif isinstance(self.value, IntID):
            if not isinstance(self.value.value, int) or self.value.value <= 0:
                raise ValueError(f"Invalid integer ID. Must be a positive integer: {self.value.value}")
        elif isinstance(self.value, StringID):
            if not isinstance(self.value.value, str) or not self.value.value.strip():
                raise ValueError(f"Invalid string ID. Must be a non-empty string: {self.value.value}")
        else:
            raise TypeError(f"Unsupported ID type: {type(self.value)}")
        return True
