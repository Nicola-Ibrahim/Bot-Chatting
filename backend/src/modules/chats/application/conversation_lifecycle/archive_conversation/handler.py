from __future__ import annotations

from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.domain.interfaces.conversation_repository import BaseConversationRepository

from .command import ArchiveConversationCommand


class ArchiveConversationHandler(BaseCommandHandler):
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def handle(self, command: BaseCommand) -> None:
        assert isinstance(command, ArchiveConversationCommand)

        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        conversation.archive()
        self._conversations.update(conversation)
