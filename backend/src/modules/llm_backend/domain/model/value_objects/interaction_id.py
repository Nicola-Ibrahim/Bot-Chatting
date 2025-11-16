from uuid import UUID

from src.building_blocks.domain.value_object import ValueObject


@dataclass
class InteractionId(ValueObject):
    id: UUID

    @classmethod
    def create(cls, id: UUID) -> "InteractionId":
        return cls(id=id)
