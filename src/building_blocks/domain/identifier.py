from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar
from uuid import UUID, uuid4

from .value_object import ValueObject


class ID(ABC):
    """Abstract base class for identifiers."""

    @abstractmethod
    def validate(self) -> None:
        """Validate the identifier."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return the string representation of the identifier."""
        pass

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Check equality based on the identifier value."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Return the hash of the identifier."""
        pass


@dataclass(frozen=True)
class UUID4ID(ID):
    """UUID4 based identifier."""

    value: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate the UUID4 identifier."""
        try:
            UUID(self.value, version=4)
        except ValueError:
            raise ValueError(f"Invalid UUID4 identifier: {self.value}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UUID4ID):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class IntID(ID):
    """Integer based identifier."""

    value: int

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate the integer identifier."""
        if not isinstance(self.value, int):
            raise ValueError(f"Invalid integer identifier: {self.value}")

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, IntID):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass(frozen=True)
class StringID(ID):
    """String based identifier."""

    value: str

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Validate the string identifier."""
        if not isinstance(self.value, str):
            raise ValueError(f"Invalid string identifier: {self.value}")

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StringID):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


IDType = TypeVar("IDType", bound=ID)


@dataclass(frozen=True)
class Identifier(ValueObject):
    value: IDType = field(default_factory=UUID4ID)

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
            if not isinstance(self.value.value, str):
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
