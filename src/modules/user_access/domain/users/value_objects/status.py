from dataclasses import dataclass, field

from src.building_blocks.domain.value_object import ValueObject

from ..enums.user_registration_status import UserRegisterationStatus


@dataclass(frozen=True)
class Status(ValueObject):
    value: UserRegisterationStatus = field(default_factory=UserRegisterationStatus.PENDING)
