import uuid
from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class MessageId(ValueObject):
    """
    Represents the ID of a message.
    """

    value: uuid.UUID

    @classmethod
    def create(cls, value: uuid.UUID) -> "MessageId":
        """
        Creates a new instance of the MessageId class.

        Args:
            value (uuid.UUID): The value of the message ID.

        Returns:
            MessageId: A new instance of the MessageId class.
        """
        return cls(value=value)
