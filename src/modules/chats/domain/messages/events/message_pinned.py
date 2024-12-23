import uuid
from dataclasses import dataclass

from ......building_blocks.domain.domain_event import DomainEvent


class MessageEvent(DomainEvent):
    @property
    def namespace(self) -> str:
        return "message"


@dataclass
class MessagePinedEvent(MessageEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID


@dataclass
class MessageAddedEvent(DomainEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID


@dataclass
class MessageUpdatedEvent(DomainEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID
    content_id: uuid.UUID
