import uuid

from ...contracts.base_command import BaseCommand


class DeleteConversationCommand(BaseCommand):
    conversation_id: uuid.UUID

    class Config:
        schema_extra = {"example": {"conversation_id": "123e4567-e89b-12d3-a456-426614174000"}}
