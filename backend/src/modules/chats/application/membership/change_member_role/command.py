import uuid

from src.modules.chats.application.contracts.command import BaseCommand


class ChangeMemberRoleCommand(BaseCommand):
    conversation_id: uuid.UUID
    member_id: uuid.UUID
    role: str
