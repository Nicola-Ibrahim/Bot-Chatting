import uuid
from dataclasses import dataclass, field

from src.building_blocks.domain.aggregate_root import AggregateRoot
from src.building_blocks.domain.exceptions import BusinessRuleValidationException

from ..members.value_objects.member_id import MemberId
from ..messages.value_objects.message_id import MessageId
from .entities.creator import Creator
from .entities.participant import Participant
from .enums.participant_role import ParticipantRole
from .events import (
    ConversationArchivedEvent,
    ConversationDeletedEvent,
    ConversationRenamedEvent,
    ConversationSharedEvent,
    ConversationTitleUpdatedEvent,
    MessageAddedEvent,
    ParticipantAddedEvent,
    ParticipantRoleChangedEvent,
)
from .rules import (
    ConversationCannotBeDeletedIfArchivedRule,
    ConversationCannotBeModifiedIfArchivedRule,
    ConversationCannotBeRenamedIfArchivedRule,
    ConversationCannotBeSharedIfArchivedRule,
    CreatorCannotBeRemovedRule,
    MessageCannotBeAddedIfArchivedRule,
    ParticipantCannotBeAddedIfAlreadyExistsRule,
    ParticipantCannotBeRemovedIfNotExistsRule,
    TitleCannotBeEmptyRule,
)
from .value_objects.conversation_id import ConversationId


@dataclass
class Conversation(AggregateRoot):
    _id: ConversationId
    _title: str
    _creator: Creator
    _participants: list[Participant] = field(default_factory=list)
    _message_ids: list[MessageId] = field(default_factory=list)
    _is_archived: bool = field(default=False, init=False)

    # ---------------------------------------------------------------------
    # Properties
    #
    @property
    def id(self) -> uuid.UUID:
        """Return the underlying UUID value for this conversation's identifier."""
        return self._id.value

    @property
    def title(self) -> str:
        """Return the conversation title."""
        return self._title

    @property
    def creator(self) -> Creator:
        """Return the creator entity."""
        return self._creator

    @property
    def participants(self) -> list[Participant]:
        """Return the list of participants in the conversation."""
        return list(self._participants)

    @property
    def message_ids(self) -> list[MessageId]:
        """Return the list of message identifiers associated with the conversation."""
        return list(self._message_ids)

    @property
    def is_archived(self) -> bool:
        """Indicate whether the conversation has been archived."""
        return self._is_archived

    @classmethod
    def create(cls, creator_id: MemberId, creator_name: str, title: str) -> "Conversation":
        """
        Creates a new conversation.

        Args:
            creator_id (MemberId): The ID of the user creating the conversation.
            creator_name (str): The name of the user creating the conversation.
            title (str): The title of the conversation.

        Returns:
            Conversation: The newly created conversation.
        """
        # Validate the title before creating the aggregate
        if TitleCannotBeEmptyRule(title).is_broken():
            raise BusinessRuleValidationException(TitleCannotBeEmptyRule(title))
        # Validate the creator's name
        if creator_name is None or not creator_name.strip():
            raise BusinessRuleValidationException("Creator name cannot be empty")

        creator = Creator.create(member_id=creator_id, name=creator_name)
        return cls(_id=ConversationId.create(id=uuid.uuid4()), _title=title, _creator=creator)

    def add_participant(self, participant_id: MemberId, role: ParticipantRole) -> None:
        """
        Adds a participant to the conversation with a specific role.

        Args:
            participant_id (MemberId): The ID of the user to be added as a participant.
            role (ParticipantRole): The role assigned to the participant.

        Raises:
            BusinessRuleValidationException: If the conversation is archived or the participant already exists.
        """
        self.check_rules(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))
        self.check_rules(
            ParticipantCannotBeAddedIfAlreadyExistsRule(participants=self._participants, participant_id=participant_id)
        )

        participant = Participant.create(participant_id=participant_id, conversation_id=self._id, role=role)
        self._participants.append(participant)

        self.add_event(ParticipantAddedEvent(conversation_id=self._id, participant_id=participant_id))

    def remove_participant(self, participant_id: MemberId) -> None:
        """
        Removes a participant from the conversation.

        Args:
            participant_id (MemberId): The ID of the user to be removed.

        Raises:
            BusinessRuleValidationException: If the conversation is archived, the participant does not exist, or the participant is the creator.
        """
        self.check_rules(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))
        self.check_rules(
            ParticipantCannotBeRemovedIfNotExistsRule(participants=self._participants, participant_id=participant_id)
        )
        # Ensure we are not removing the creator
        self.check_rules(CreatorCannotBeRemovedRule(creator_id=self._creator.id, participant_id=participant_id))

        participant = next((p for p in self._participants if p.id == participant_id), None)
        self._participants.remove(participant)
        participant.remove()

    def change_participant_role(self, participant_id: MemberId, new_role: ParticipantRole) -> None:
        """
        Changes the role of a participant in the conversation.

        Args:
            participant_id (MemberId): The ID of the user whose role is to be changed.
            new_role (ParticipantRole): The new role to be assigned to the participant.

        Raises:
            BusinessRuleValidationException: If the conversation is archived or the participant does not exist.
        """
        self.check_rules(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))

        participant = next((p for p in self._participants if p.id == participant_id), None)
        if participant:
            participant.change_role(new_role)
            self.add_event(
                ParticipantRoleChangedEvent(conversation_id=self._id, participant_id=participant_id, new_role=new_role)
            )
        else:
            raise BusinessRuleValidationException(f"User {participant_id} is not a participant.")

    def archive(self) -> None:
        """
        Archives the conversation.

        Raises:
            BusinessRuleValidationException: If the conversation is already archived.
        """
        if self._is_archived:
            raise BusinessRuleValidationException("Conversation is already archived.")
        self._is_archived = True
        self.add_event(ConversationArchivedEvent(conversation_id=self._id))

    def delete(self) -> None:
        """
        Deletes the conversation.

        Raises:
            BusinessRuleValidationException: If the conversation is archived.
        """
        self.check_rules(ConversationCannotBeDeletedIfArchivedRule(is_archived=self._is_archived))
        self.add_event(ConversationDeletedEvent(conversation_id=self._id))

    # ------------------------------------------------------------------
    # Additional domain behaviours
    #
    def rename(self, new_title: str) -> None:
        """
        Rename or update the conversation's title.

        This method enforces that the conversation cannot be renamed once
        archived and that the new title is not empty. On success it
        updates the internal title and emits a ``ConversationTitleUpdatedEvent``.

        Args:
            new_title: The new title to assign to the conversation.

        Raises:
            BusinessRuleValidationException: If the conversation is archived
                or the new title is empty.
        """
        # Disallow renaming if archived
        self.check_rules(ConversationCannotBeRenamedIfArchivedRule(is_archived=self._is_archived))
        # Validate the new title is not empty
        if TitleCannotBeEmptyRule(new_title).is_broken():
            raise BusinessRuleValidationException(TitleCannotBeEmptyRule(new_title))

        # Apply the state change and emit an event
        self._title = new_title
        self.add_event(ConversationTitleUpdatedEvent(conversation_id=self._id.value, new_title=new_title))

    def share(self, user_id: str) -> None:
        """
        Share this conversation with another user.

        Sharing a conversation does not currently change any internal
        state of the aggregate but emits a ``ConversationSharedEvent`` to
        signal that sharing has occurred. Archived conversations cannot
        be shared.

        Args:
            user_id: The identifier of the user with whom the conversation
                is being shared.

        Raises:
            BusinessRuleValidationException: If the conversation is archived.
        """
        self.check_rules(ConversationCannotBeSharedIfArchivedRule(is_archived=self._is_archived))
        # No state change required; event records the action
        self.add_event(ConversationSharedEvent(conversation_id=self._id.value, user_id=user_id))

    def add_message_id(self, message_id: MessageId) -> None:
        """
        Associate a new message with this conversation.

        In a DDD design the ``Message`` aggregate is managed separately,
        however the ``Conversation`` tracks the identifiers of messages
        belonging to it. This method appends the provided message ID
        while checking that the conversation has not been archived. An
        appropriate ``MessageAddedEvent`` is emitted.

        Args:
            message_id: The ``MessageId`` of the message being added.

        Raises:
            BusinessRuleValidationException: If the conversation is archived.
        """
        self.check_rules(MessageCannotBeAddedIfArchivedRule(is_archived=self._is_archived))
        self._message_ids.append(message_id)
        self.add_event(MessageAddedEvent(conversation_id=self._id.value, message_id=message_id.value))
