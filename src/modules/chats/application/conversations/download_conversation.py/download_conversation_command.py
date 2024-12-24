from uuid import UUID

from ...contracts.base_command import BaseCommand


class DownloadConversationCommand(BaseCommand):
    conversation_id: UUID
