"""Membership Service."""

from __future__ import annotations

import uuid

from ...domain.conversations.enums.participant_role import ParticipantRole
from ...domain.interfaces.conversation_repository import BaseConversationRepository
from ...domain.members.value_objects.member_id import MemberId
from .add_member_command import AddMemberCommand
from .change_member_role_command import ChangeMemberRoleCommand
from .remove_member_command import RemoveMemberCommand


class MembershipService:
    def __init__(self, conversation_repository: BaseConversationRepository) -> None:
        self._conversations = conversation_repository

    def add(self, command: AddMemberCommand) -> None:
        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        participant_id = MemberId.create(uuid.UUID(str(command.member_id)))
        role = ParticipantRole(command.role)
        conversation.add_participant(participant_id, role)
        self._conversations.update(conversation)

    def change_role(self, command: ChangeMemberRoleCommand) -> None:
        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        participant_id = MemberId.create(uuid.UUID(str(command.member_id)))
        new_role = ParticipantRole(command.role)
        conversation.change_participant_role(participant_id, new_role)
        self._conversations.update(conversation)

    def remove(self, command: RemoveMemberCommand) -> None:
        conversation = self._conversations.find(command.conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        participant_id = MemberId.create(uuid.UUID(str(command.member_id)))
        conversation.remove_participant(participant_id)
        self._conversations.update(conversation)
