import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class ConversationArchivedEvent(DomainEvent):
    conversation_id: uuid.UUID
