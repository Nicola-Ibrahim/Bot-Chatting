import uuid
from dataclasses import dataclass

from building_blocks.domain.events import DomainEvent


@dataclass
class ConversationTitleUpdatedEvent(DomainEvent):
    conversation_id: uuid.UUID
    new_title: str
