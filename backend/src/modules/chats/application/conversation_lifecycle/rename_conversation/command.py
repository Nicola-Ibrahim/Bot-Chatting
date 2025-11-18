import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class RenameConversationCommand(BaseCommand):
    conversation_id: uuid.UUID
    title: str
