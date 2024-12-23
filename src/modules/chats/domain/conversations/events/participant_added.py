import uuid
from dataclasses import dataclass

from ......building_blocks.domain.domain_event import DomainEvent


@dataclass
class ParticipantAddedEvent(DomainEvent):
    conversation_id: uuid.UUID
    participant_id: str
    permission: str
    participant_id: str
    permission: str
    permission: str
    participant_id: str
    permission: str
