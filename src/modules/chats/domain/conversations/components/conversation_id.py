import uuid
from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject


@dataclass(frozen=True)
class ConversationId(ValueObject):
    _value: uuid.UUID

    @classmethod
    def create(cls, id: uuid.UUID) -> "ConversationId":
        return cls(_value=id)

    @property
    def value(self) -> uuid.UUID:
        return self._value
