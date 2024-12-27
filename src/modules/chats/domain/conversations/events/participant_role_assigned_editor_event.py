import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class ParticipantRoleAssignedEditorEvent(DomainEvent):
    participant_id: uuid.UUID
    conversation_id: uuid.UUID
