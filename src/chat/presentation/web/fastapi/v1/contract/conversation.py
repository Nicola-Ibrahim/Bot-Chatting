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
