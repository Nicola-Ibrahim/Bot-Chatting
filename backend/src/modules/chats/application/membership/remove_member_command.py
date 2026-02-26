import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class RemoveMemberCommand(BaseCommand):
    conversation_id: uuid.UUID
    member_id: uuid.UUID
