from __future__ import annotations

import uuid

from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.application.messaging.send_message.dto import SentMessageDTO
from src.modules.chats.domain.conversations.value_objects.conversation_id import ConversationId
from src.modules.chats.domain.members.value_objects.member_id import MemberId
from src.modules.chats.domain.messages.interfaces.repository import AbstractMessageRepository
from src.modules.chats.domain.messages.interfaces.response_generator import ResponseGenerator
from src.modules.chats.domain.messages.root import Message
from src.modules.chats.domain.messages.value_objects.content import Content
from src.modules.chats.domain.messages.value_objects.message_id import MessageId

from .command import SendMessageCommand


class SendMessageHandler(BaseCommandHandler):
    def __init__(
        self,
        messages_repository: AbstractMessageRepository,
        response_generator: ResponseGenerator,
    ) -> None:
        self._messages_repository = messages_repository
        self._response_generator = response_generator

    def handle(self, command: BaseCommand) -> Message | SentMessageDTO:
        assert isinstance(command, SendMessageCommand)

        # Generate a response based on the request text
        response = self._response_generator.generate_answer(command.text)

        conversation_id = ConversationId.create(command.conversation_id)
        sender_id = MemberId.create(command.sender_id)
        content = Content.create(text=command.text, response=response)

        message = Message.create(
            message_id=MessageId.create(),
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
        )

        self._messages_repository.save(message=message)
        return SentMessageDTO(
            message_id=str(message._id.value),  # noqa: SLF001
            conversation_id=str(conversation_id.value),
            sender_id=str(sender_id.value),
        )
