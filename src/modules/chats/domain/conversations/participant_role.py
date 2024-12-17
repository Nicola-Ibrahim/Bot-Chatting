from dataclasses import dataclass
from enum import Enum

from src.building_blocks.domain.value_object import ValueObject


class Role(Enum):
    EDITOR = "Editor"
    VIEWER = "Viewer"


@dataclass
class ConversationRole(ValueObject):
    _role: Role

    @classmethod
    def editor(cls):
        return cls(_role=Role.EDITOR)

    @classmethod
    def viewer(cls):
        return cls(_role=Role.VIEWER)
