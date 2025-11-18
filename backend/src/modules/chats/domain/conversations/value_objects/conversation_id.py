from dataclasses import dataclass
from uuid import UUID

from src.building_blocks.domain.value_object import ValueObject


@dataclass
class ConversationId(ValueObject):
    value: UUID

    @classmethod
    def create(cls, id: UUID) -> "ConversationId":
        return cls(value=id)
