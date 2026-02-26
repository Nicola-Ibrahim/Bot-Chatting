"""Conversation Lifecycle Service."""

from __future__ import annotations

from ...domain.conversations.conversation import Conversation
from ...domain.interfaces.conversation_repository import BaseConversationRepository
from ...domain.members.value_objects.member_id import MemberId
from .archive_conversation_command import ArchiveConversationCommand
from .rename_conversation_command import RenameConversationCommand
from .start_conversation_command import StartConversationCommand
from .start_conversation_dto import ConversationStartedDTO


class ConversationLifecycleService:
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def start(self, command: StartConversationCommand) -> ConversationStartedDTO:
        creator_id = MemberId.create(command.user_id)
        conversation = Conversation.create(creator_id=creator_id, creator_name=command.user_name, title=command.title)
        self._conversations.save(conversation)
        return ConversationStartedDTO(conversation_id=str(conversation.id), title=conversation.title)

    def archive(self, command: ArchiveConversationCommand) -> None:
        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        conversation.archive()
        self._conversations.update(conversation)

    def rename(self, command: RenameConversationCommand) -> None:
        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        conversation.rename(command.title)
        self._conversations.update(conversation)
