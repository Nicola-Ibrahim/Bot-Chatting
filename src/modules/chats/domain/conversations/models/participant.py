import uuid
from dataclasses import dataclass

from participant_role import Role

from src.building_blocks.domain.entity import Entity


@dataclass
class Participant(Entity):
    _user_id: uuid.UUID
    _conversation_id: uuid.UUID
    _role: Role
    _is_removed: bool = False

    @classmethod
    def create(cls, user_id: uuid.UUID, conversation_id: uuid.UUID, role: Role):
        return cls(_user_id=user_id, _conversation_id=conversation_id, _role=role)
