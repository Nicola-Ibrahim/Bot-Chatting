from uuid import UUID

from pydantic import BaseModel, Field

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.conversations.root import Conversation
from src.modules.chats.domain.messages.root import Message
from src.modules.chats.domain.value_objects import Content

from ..contracts.command_base import CommandBase


class AddMessageToConversationCommand(CommandBase[Result[ConversationDTO, str]]):
    conversation_id: UUID
    text: str = Field(..., min_length=1, max_length=5000)

    class Config:
        schema_extra = {
            "example": {"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "text": "Hello, how are you?"}
        }
