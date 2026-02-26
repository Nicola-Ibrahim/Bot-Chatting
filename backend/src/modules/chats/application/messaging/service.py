"""Messaging Service."""

from __future__ import annotations

import uuid

from ...domain.conversations.value_objects.conversation_id import ConversationId
from ...domain.members.value_objects.member_id import MemberId
from ...domain.messages.interfaces.repository import AbstractMessageRepository
from ...domain.messages.interfaces.response_generator import ResponseGenerator
from ...domain.messages.root import Message
from ...domain.messages.value_objects.content import Content
from ...domain.messages.value_objects.message_id import MessageId
from .delete_message_command import DeleteMessageCommand
from .edit_message_command import EditMessageCommand
from .send_message_command import SendMessageCommand
from .send_message_dto import SentMessageDTO


class MessagingService:
    def __init__(
        self,
        messages_repository: AbstractMessageRepository,
        response_generator: ResponseGenerator,
    ) -> None:
        self._messages_repository = messages_repository
        self._response_generator = response_generator

    def send(self, command: SendMessageCommand) -> Message | SentMessageDTO:
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

    def edit(self, command: EditMessageCommand) -> Message:
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

    def delete(self, command: DeleteMessageCommand) -> None:
        self._messages_repository.delete(str(command.message_id))
