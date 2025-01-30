import uuid
from dataclasses import dataclass, field
from typing import Self

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class MessageId(ValueObject):
    """
    Represents the ID of a message.
    """

    value: uuid.UUID

    @property
    def id(self) -> uuid.UUID:
        return self.value

    @classmethod
    def create(cls, value: uuid.UUID = field(default_factory=uuid.uuid4)) -> Self:
        """
        Creates a new instance of the MessageId class.

        Args:
            value (uuid.UUID, optional): The value of the message ID. Defaults to a new UUID.

        Returns:
            MessageId: A new instance of the MessageId class.
        """
        # If there are any specific business rules for MessageId, they should be checked here
        return cls(value=value)
