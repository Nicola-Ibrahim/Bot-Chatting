import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.entity import AggregateRoot

from ..messages.root import Message
from .content import Content
from .events.participant_added import ParticipantAddedEvent
from .owner import Owner
from .participant import Participant
from .participant_role import Role


@dataclass
class Conversation(AggregateRoot):
    _message_ids: list[uuid.UUID] = field(default_factory=list)
    _owner: Owner
    _participants: list[Participant] = field(default_factory=list)
    _title: str = ""

    def add_participant(self, user_id: str, role: Role):
        """
        Adds a participant to the conversation with a specific permission.
        """

        self.check_rule(MeetingCannotBeChangedAfterStartRule(_term))
        self.check_rule(AttendeeCanBeAddedOnlyInRsvpTermRule(_rsvpTerm))

        self._participants.append(Participant.create(user_id=user_id, conversation_id=self._id, role=role))

        # Raise the domain event
        event = ParticipantAddedEvent(
            conversation_id=self._id,
            participant_id=user_id,
        )
        self._record_event(event)

    def remove_participant(self, user_id: str):
        if user_id not in self._participants:
            raise ValueError(f"User {user_id} is not a participant.")
        del self._participants[user_id]

    def add_message(self, message_id: uuid.UUID):
        """
        Adds a message ID to the conversation's list of messages.
        """
        self._message_ids.append(message_id)

        # Raise the domain event
        event = MessageAddedEvent(
            conversation_id=self._id,
            message_id=message_id,
        )
        self._record_event(event)

    def remove_message(self, message_id: uuid.UUID):
        """
        Removes a message from the conversation.
        """
        self._message_ids.remove(message_id)

        # Raise the domain event
        event = MessageRemovedEvent(
            conversation_id=self._id,
            message_id=message_id,
            timestamp=str(datetime.now()),
        )
        self._record_event(event)

    def get_message_ids(self):
        return self._message_ids

    def get_last_n_messages(self, n: int):
        """
        Retrieves the last `n` messages in the conversation.
        """
        if n <= 0:
            raise ValueError("Number of messages must be positive.")
        return list(self._messages.values())[-n:]

    def read_chat_partially(self, tokenizer, max_recent: int = 5, token_limit: int = 500):
        """
        Retrieves recent messages from the conversation within a token limit.
        """
        last_messages = self.get_last_n_messages(max_recent)
        selected_messages = []
        total_tokens = 0

        for message in reversed(last_messages):
            tokens = message.tokenize_message(tokenizer)
            if total_tokens + tokens > token_limit:
                break

            selected_messages.insert(0, message)
            total_tokens += tokens

        # Raise the domain event
        event = MessagesRetrievedEvent(
            conversation_id=self._id,
            retrieved_message_ids=[msg.id for msg in selected_messages],
            token_count=total_tokens,
            timestamp=str(datetime.now()),
        )
        self._record_event(event)

        return selected_messages
