import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent

from ..participant_role import Role


@dataclass
class ParticipantRoleChangedEvent(DomainEvent):
    conversation_id: uuid.UUID
    participant_id: str
    new_role: Role
