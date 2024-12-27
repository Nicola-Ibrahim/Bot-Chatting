import uuid
from dataclasses import dataclass

from src.building_blocks.domain.events import DomainEvent


@dataclass
class ConversationSharedEvent(DomainEvent):
    conversation_id: uuid.UUID
    user_id: str
