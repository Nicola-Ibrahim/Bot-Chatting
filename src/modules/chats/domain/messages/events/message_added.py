import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class MessageAddedEvent(DomainEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID
