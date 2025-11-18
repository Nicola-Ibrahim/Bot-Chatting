import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class DeleteMessageCommand(BaseCommand):
    message_id: uuid.UUID
