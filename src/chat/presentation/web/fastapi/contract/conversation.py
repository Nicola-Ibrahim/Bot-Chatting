import uuid

from pydantic import BaseModel


class ConversationViewModel(BaseModel):

    id: uuid
    name: str


class MessageResponseSchema(BaseModel):
    id: uuid
    text: str
    response: str
    feedback: str


class ConversationResponseSchema(BaseModel):
    id: uuid
    messages: list[MessageResponseSchema]
