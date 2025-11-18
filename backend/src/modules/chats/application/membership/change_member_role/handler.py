from __future__ import annotations

import uuid

from src.modules.chats.application.configuration.command_handler import BaseCommandHandler
from src.modules.chats.application.contracts.command import BaseCommand
from src.modules.chats.domain.conversations.enums.participant_role import ParticipantRole
from src.modules.chats.domain.interfaces.conversation_repository import BaseConversationRepository
from src.modules.chats.domain.members.value_objects.member_id import MemberId

from .command import ChangeMemberRoleCommand


class ChangeMemberRoleHandler(BaseCommandHandler):
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def handle(self, command: BaseCommand) -> None:
        assert isinstance(command, ChangeMemberRoleCommand)

        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        participant_id = MemberId.create(uuid.UUID(str(command.member_id)))
        new_role = ParticipantRole(command.role)
        conversation.change_participant_role(participant_id, new_role)
        self._conversations.update(conversation)
