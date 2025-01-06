import uuid
from dataclasses import dataclass, field

from src.building_blocks.domain.entity import AggregateRoot

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
    _title: str = ""
    _creator: Creator
    _participants: list[Participant] = field(default_factory=list)
    _message_ids: list[MessageId] = field(default_factory=list)
    _is_archived: bool = False

    @property
    def title(self) -> str:
        """
        Retrieves the title of the conversation.

        Returns:
            str: The title of the conversation.
        """
        return self._title

    @property
    def creator(self) -> Creator:
        """
        Retrieves the creator of the conversation.

        Returns:
            Creator: The creator of the conversation.
        """
        return self._creator

    @property
    def is_archived(self) -> bool:
        """
        Retrieves the archived status of the conversation.

        Returns:
            bool: True if the conversation is archived, False otherwise.
        """
        return self._is_archived

    @classmethod
    def create(cls, creator_id: MemberId, user_name: str, title: str) -> "Conversation":
        """
        Creates a new conversation.

        Args:
            creator_id (MemberId): The ID of the user creating the conversation.
            user_name (str): The name of the user creating the conversation.
            title (str): The title of the conversation.

        Returns:
            Conversation: The newly created conversation.
        """
        creator = Creator.create(member_id=creator_id, name=user_name)
        conversation = cls(_id=ConversationId.create(id=uuid.uuid4()), _title=title, _creator=creator)
        return conversation

    def add_participant(self, participant_id: MemberId, role: ParticipantRole):
        """
        Adds a participant to the conversation with a specific role.

        Args:
            participant_id (MemberId): The ID of the user to be added as a participant.
            role (ParticipantRole): The role assigned to the participant.

        Raises:
            ValueError: If the conversation is archived or the participant already exists.
        """
        self.check_rule(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))
        self.check_rule(
            ParticipantCannotBeAddedIfAlreadyExistsRule(participants=self._participants, participant_id=participant_id)
        )

        self._participants.append(
            Participant.create(participant_id=participant_id, conversation_id=self._id, role=role)
        )

        # Raise the domain event
        event = ParticipantAddedEvent(
            conversation_id=self._id,
            participant_id=participant_id,
        )
        self.add_event(event)

    def remove_participant(self, participant_id: MemberId):
        """
        Removes a participant from the conversation.

        Args:
            participant_id (MemberId): The ID of the user to be removed.

        Raises:
            ValueError: If the conversation is archived, the participant does not exist, or the participant is the creator.
        """
        self.check_rule(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))
        self.check_rule(
            ParticipantCannotBeRemovedIfNotExistsRule(participants=self._participants, participant_id=participant_id)
        )
        self.check_rule(CreatorNameCannotBeEmptyRule(creator_id=self._creator.id, participant_id=participant_id))

        participant = next((p for p in self._participants if p.id == participant_id), None)
        self._participants.remove(participant)
        participant.remove()

    def change_participant_role(self, participant_id: MemberId, new_role: ParticipantRole):
        """
        Changes the role of a participant in the conversation.

        Args:
            participant_id (MemberId): The ID of the user whose role is to be changed.
            new_role (ParticipantRole): The new role to be assigned to the participant.

        Raises:
            ValueError: If the conversation is archived or the participant does not exist.
        """
        self.check_rule(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))

        participant = next((p for p in self._participants if p._user_id == participant_id), None)
        if participant:
            participant.change_role(new_role)
            # Raise the domain event
            event = ParticipantRoleChangedEvent(
                conversation_id=self._id,
                participant_id=participant_id,
                new_role=new_role,
            )
            self.add_event(event)
        else:
            raise ValueError(f"User {participant_id} is not a participant.")

    def get_participant(self, participant_id: MemberId) -> Participant:
        """
        Retrieves a participant from the conversation by user ID.

        Args:
            participant_id (MemberId): The ID of the user to be retrieved.

        Returns:
            Participant: The participant with the specified user ID, or None if not found.
        """
        return next((p for p in self._participants if p._user_id == participant_id), None)

    def get_participants_by_role(self, role: ParticipantRole) -> list[Participant]:
        """
        Retrieves participants from the conversation by role.

        Args:
            role (ParticipantRole): The role to filter participants by.

        Returns:
            list[Participant]: A list of participants with the specified role.
        """
        return [p for p in self._participants if p.role == role]

    def add_message(self, message_id: MessageId):
        """
        Adds a message ID to the conversation's list of messages.

        Args:
            message_id (MessageId): The ID of the message to be added.

        Raises:
            ValueError: If the conversation is archived.
        """
        self.check_rule(MessageCannotBeAddedIfArchivedRule(is_archived=self._is_archived))

        self._message_ids.append(message_id)

        # Raise the domain event
        event = MessageAddedEvent(
            conversation_id=self._id,
            message_id=message_id,
        )
        self.add_event(event)

    def remove_message(self, message_id: MessageId):
        """
        Removes a message ID from the conversation's list of messages.

        Args:
            message_id (MessageId): The ID of the message to be removed.

        Raises:
            ValueError: If the conversation is archived or the message does not exist.
        """
        self.check_rule(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))

        if message_id not in self._message_ids:
            raise ValueError(f"Message {message_id} is not in the conversation.")
        self._message_ids.remove(message_id)

    def get_message_id(self, message_id: MessageId) -> MessageId:
        """
        Retrieves a message ID from the conversation by message ID.

        Args:
            message_id (MessageId): The ID of the message to be retrieved.

        Returns:
            MessageId: The message ID, or None if not found.
        """
        return next((m for m in self._message_ids if m == message_id), None)

    def get_message_ids(self) -> list[MessageId]:
        """
        Retrieves all message IDs from the conversation.

        Returns:
            list[MessageId]: A list of all message IDs in the conversation.
        """
        return self._message_ids

    def get_last_n_messages(self, n: int) -> list[MessageId]:
        """
        Retrieves the last N message IDs from the conversation.

        Args:
            n (int): The number of message IDs to retrieve.

        Returns:
            list[MessageId]: A list of the last N message IDs in the conversation.
        """
        return self._message_ids[-n:]

    def read_chat_partially(self, tokenizer, max_recent: int = 5, token_limit: int = 500):
        """
        Reads the chat partially based on the tokenizer, max recent messages, and token limit.

        Args:
            tokenizer: The tokenizer to use for reading the chat.
            max_recent (int, optional): The maximum number of recent messages to read. Defaults to 5.
            token_limit (int, optional): The token limit for reading the chat. Defaults to 500.
        """
        # Implementation of partial chat reading
        pass

    def update_title(self, new_title: str):
        """
        Updates the title of the conversation.

        Args:
            new_title (str): The new title of the conversation.

        Raises:
            ValueError: If the conversation is archived or the title is empty.
        """
        self.check_rule(ConversationCannotBeModifiedIfArchivedRule(is_archived=self._is_archived))
        self.check_rule(TitleCannotBeEmptyRule(title=new_title))

        self._title = new_title

        # Raise the domain event
        event = ConversationTitleUpdatedEvent(
            conversation_id=self._id,
            new_title=new_title,
        )
        self.add_event(event)

    def get_viewers(self) -> list[Participant]:
        """
        Retrieves the viewers of the conversation.

        Returns:
            list[Participant]: A list of viewers in the conversation.
        """
        return [p for p in self._participants if p.is_viewer]

    def get_editors(self):
        """
        Retrieves the editors of the conversation.

        Returns:
            list[Participant]: A list of editors in the conversation.
        """
        return [p for p in self._participants if p.is_editor]

    def archive(self):
        """
        Archives the conversation.

        Raises:
            ValueError: If the conversation is already archived.
        """
        if self._is_archived:
            raise ValueError("Conversation is already archived.")
        self._is_archived = True

        # Raise the domain event
        event = ConversationArchivedEvent(conversation_id=self._id)
        self.add_event(event)

    def delete(self):
        """
        Deletes the conversation.

        Raises:
            ValueError: If the conversation is archived.
        """
        self.check_rule(ConversationCannotBeDeletedIfArchivedRule(is_archived=self._is_archived))

        # Raise the domain event
        event = ConversationDeletedEvent(conversation_id=self._id)
        self.add_event(event)

    def share(self, member_id: str):
        """
        Shares the conversation with another user.

        Args:
            member_id (str): The ID of the user to share the conversation with.

        Raises:
            ValueError: If the conversation is archived.
        """
        self.check_rule(ConversationCannotBeSharedIfArchivedRule(is_archived=self._is_archived))

        # Raise the domain event
        event = ConversationSharedEvent(conversation_id=self._id, member_id=member_id)
        self.add_event(event)

    def rename(self, new_name: str):
        """
        Renames the conversation.

        Args:
            new_name (str): The new name of the conversation.

        Raises:
            ValueError: If the conversation is archived or the new name is empty.
        """
        self.check_rule(ConversationCannotBeRenamedIfArchivedRule(is_archived=self._is_archived))
        self.check_rule(TitleCannotBeEmptyRule(title=new_name))

        self._title = new_name

        # Raise the domain event
        event = ConversationRenamedEvent(conversation_id=self._id, new_name=new_name)
        self.add_event(event)
