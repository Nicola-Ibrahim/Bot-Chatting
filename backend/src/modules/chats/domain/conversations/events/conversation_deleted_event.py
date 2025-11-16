import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class ConversationDeletedEvent(DomainEvent):
    conversation_id: uuid.UUID
