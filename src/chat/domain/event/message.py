import uuid
from dataclasses import dataclass

from .base import DomainEvent


class MessageEvent(DomainEvent):
    @property
    def namespace(self) -> str:
        return "message"


@dataclass
class MessageAddedEvent(MessageEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID
    timestamp: str


@dataclass
class MessageUpdatedEvent(MessageEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID


@dataclass
class MessagePinedEvent(MessageEvent):
    conversation_id: uuid.UUID
    message_id: uuid.UUID
