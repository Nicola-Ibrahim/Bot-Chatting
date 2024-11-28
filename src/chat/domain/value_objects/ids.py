import uuid
from dataclasses import dataclass, field

from src.shared.domain.value_object import ValueObject


@dataclass(frozen=True)
class ConversationId(ValueObject):
    value: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def of(cls, conversation_uuid: uuid.UUID):
        return cls(value=conversation_uuid)


@dataclass(frozen=True)
class MessageId(ValueObject):
    value: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def of(cls, message_uuid: uuid.UUID):
        return cls(value=message_uuid)
