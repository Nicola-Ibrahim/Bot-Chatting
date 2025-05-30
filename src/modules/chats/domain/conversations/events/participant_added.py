import uuid
from dataclasses import dataclass

from building_blocks.domain.events import DomainEvent


@dataclass
class ParticipantAddedEvent(DomainEvent):
    conversation_id: uuid.UUID
    participant_id: str
