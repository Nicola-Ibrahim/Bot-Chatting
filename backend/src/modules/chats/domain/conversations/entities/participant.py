import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.entity import Entity

from ...members.value_objects.member_id import MemberId
from ..enums.participant_role import ParticipantRole
from ..events import ParticipantRoleAssignedEditorEvent, ParticipantRoleAssignedViewerEvent


@dataclass
class Participant(Entity):
    _id: MemberId
    _role: ParticipantRole
    _is_removed: bool = False
    _removed_date: datetime = field(default=None)
    _removing_reason: str = field(default=None)
    _removing_member_id: uuid.UUID = field(default=None)

    @classmethod
    def create(cls, member_id: MemberId, conversation_id: uuid.UUID, role: ParticipantRole) -> "Participant":
        """
        Creates a new participant.

        Args:
            member_id (uuid.UUID): The ID of the participant.
            conversation_id (uuid.UUID): The ID of the conversation.
            role (ParticipantRole): The role of the participant.

        Returns:
            Participant: A new participant instance.
        """
        return cls(_id=member_id, _conversation_id=conversation_id, _role=role)

    @property
    def is_removed(self) -> bool:
        """
        Checks if the participant is removed.

        Returns:
            bool: True if the participant is removed, False otherwise.
        """
        return self._is_removed

    @property
    def is_viewer(self) -> bool:
        """
        Checks if the participant is a viewer.

        Returns:
            bool: True if the participant is a viewer, False otherwise.
        """
        return self._role == ParticipantRole.VIEWER

    @property
    def is_editor(self) -> bool:
        """
        Checks if the participant is an editor.

        Returns:
            bool: True if the participant is an editor, False otherwise.
        """
        return self._role == ParticipantRole.EDITOR

    def assign_role_viewer(self) -> None:
        """
        Assigns the participant's role to viewer.
        """
        self._role = ParticipantRole.VIEWER
        self.add_event(ParticipantRoleAssignedViewerEvent(self.id, self._conversation_id))

    def assign_role_editor(self) -> None:
        """
        Assigns the participant's role to editor.
        """
        self._role = ParticipantRole.EDITOR
        self.add_event(ParticipantRoleAssignedEditorEvent(self.id, self._conversation_id))

    def remove(self, removing_member_id: uuid.UUID, reason: str) -> None:
        """
        Removes the participant from the conversation.

        Args:
            removing_member_id (uuid.UUID): The ID of the member removing the participant.
            reason (str): The reason for removing the participant.
        """

        self._is_removed = True
        self._removed_date = datetime.now()
        self._removing_reason = reason
        self._removing_member_id = removing_member_id

        self.add_event()
