from uuid import UUID

from pydantic import Field

from src.modules.chats.domain.messages.root import Message

from ...contracts.command import BaseCommand


class AddMessageToConversationCommand(BaseCommand):
    conversation_id: UUID
    text: str = Field(..., min_length=1, max_length=5000)

    class Config:
        schema_extra = {
            "example": {"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "text": "Hello, how are you?"}
        }
