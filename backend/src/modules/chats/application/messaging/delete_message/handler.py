from __future__ import annotations

from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.domain.messages.interfaces.repository import AbstractMessageRepository

from .command import DeleteMessageCommand


class DeleteMessageHandler(BaseCommandHandler):
    def __init__(self, messages_repository: AbstractMessageRepository) -> None:
        self._messages_repository = messages_repository

    def handle(self, command: BaseCommand) -> None:
        assert isinstance(command, DeleteMessageCommand)
        self._messages_repository.delete(str(command.message_id))
