import uuid
from dataclasses import dataclass, field
from typing import Self

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class MemberId(ValueObject):
    """Represents the ID of a member."""

    _value: uuid.UUID

    @property
    def value(self) -> uuid.UUID:
        return self._value

    @classmethod
    def create(cls, value: uuid.UUID = field(default_factory=uuid.uuid4)) -> Self:
        """
        Creates a new instance of the MemberId class.

        Args:
            value (uuid.UUID, optional): The value of the member ID. Defaults to a new UUID.

        Returns:
            MemberId: A new instance of the MemberId class.
        """
        return cls(_value=value)
