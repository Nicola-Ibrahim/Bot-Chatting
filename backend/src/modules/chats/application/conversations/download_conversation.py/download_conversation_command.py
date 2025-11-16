from uuid import UUID

from ...contracts.command import BaseCommand


class DownloadConversationCommand(BaseCommand):
    conversation_id: UUID
