from __future__ import annotations

import uuid

from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.domain.messages.interfaces.repository import AbstractMessageRepository
from src.modules.chats.domain.messages.interfaces.response_generator import ResponseGenerator
from src.modules.chats.domain.messages.value_objects.content import Content

from .command import EditMessageCommand


class EditMessageHandler(BaseCommandHandler):
    def __init__(
        self,
        messages_repository: AbstractMessageRepository,
        response_generator: ResponseGenerator,
    ) -> None:
        self._messages_repository = messages_repository
        self._response_generator = response_generator

    def handle(self, command: BaseCommand):
        assert isinstance(command, EditMessageCommand)

        message = self._messages_repository.get_by_id(str(command.message_id))
        if not message:
            raise ValueError("Message not found")

        response = self._response_generator.generate_answer(command.text)
        content = Content.create(text=command.text, response=response)
        conversation_id = command.conversation_id
        if conversation_id is None:
            conversation_id = getattr(message, "_conversation_id", None)
        if conversation_id is None:
            raise ValueError("Conversation id is required to edit message")

        message.append_content(content, conversation_id=uuid.UUID(str(conversation_id)))
        self._messages_repository.update(message)
        return message
