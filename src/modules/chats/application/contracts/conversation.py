import uuid
from dataclasses import dataclass
from datetime import datetime

from .dto import BaseDTO
from .message import MessageDTO


@dataclass
class ConversationDTO(BaseDTO):
    id: uuid.UUID
    messages: list[MessageDTO]
    created_at: datetime

    @classmethod
    def from_domain(cls, domain_object):
        return cls(
            id=domain_object.id,
            messages=[MessageDTO.from_domain(msg) for msg in domain_object.messages],
            created_at=domain_object.timestamp,
        )


from pydantic import BaseModel


class ConversationViewModel(BaseModel):
    id: str
    name: str


class MessageResponseSchema(BaseModel):
    id: str
    text: str
    response: str
    feedback: str


class ConversationResponseSchema(BaseModel):
    id: str
    messages: list[MessageResponseSchema]


class MessageRequestSchema(BaseModel):
    text: str
    response: str


class CreateConversationRequestSchema(BaseModel):
    messages: list[MessageRequestSchema]

    def map_to_conversation(self):
        pass
