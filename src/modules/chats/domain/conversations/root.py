import uuid
from dataclasses import dataclass, field

from src.building_blocks.domain.entity import AggregateRoot
from src.building_blocks.domain.exception import BusinessRuleValidationException

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
    CreatorNameCannotBeEmptyRule,
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
        cls.check_rules(TitleCannotBeEmptyRule(title))
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
        self.check_rules(CreatorNameCannotBeEmptyRule(creator_id=self._creator.id, participant_id=participant_id))

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
