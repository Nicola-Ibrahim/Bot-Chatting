import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class StartConversationCommand(BaseCommand):
    user_id: uuid.UUID
    user_name: str
    title: str
