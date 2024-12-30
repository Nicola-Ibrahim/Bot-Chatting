import uuid

from ....domain.conversations.root import Conversation
from ...contracts.command import BaseCommand


class CreateConversationCommand(BaseCommand[Conversation]):
    user_id: uuid.UUID
    user_name: str
    conversation_title: str = None

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_name": "John Doe",
                "conversation_title": "My conversation",
            }
        }
