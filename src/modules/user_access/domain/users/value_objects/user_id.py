import uuid

from src.building_blocks.domain.value_object import ValueObject


class UserId(ValueObject):
    _value: uuid.UUID

    @classmethod
    def create(cls, value: uuid.UUID) -> "MemberId":
        return cls(_value=value)
