import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class ArchiveConversationCommand(BaseCommand):
    conversation_id: uuid.UUID
