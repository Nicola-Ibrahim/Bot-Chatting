import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class EditMessageCommand(BaseCommand):
    message_id: uuid.UUID
    text: str
    conversation_id: uuid.UUID | None = None
