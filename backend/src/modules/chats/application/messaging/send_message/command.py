import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class SendMessageCommand(BaseCommand):
    conversation_id: uuid.UUID
    sender_id: uuid.UUID
    text: str
