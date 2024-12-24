import uuid

from src.building_blocks.domain.result import Result
from src.modules.chats.domain.conversations.root import Conversation

from ...contracts.base_command import BaseCommand


class CreateConversationCommand(BaseCommand[Result[Conversation]]):
    user_id: uuid.UUID

    class Config:
        schema_extra = {"example": {"user_id": "123e4567-e89b-12d3-a456-426614174000"}}
        schema_extra = {"example": {"user_id": "123e4567-e89b-12d3-a456-426614174000"}}
