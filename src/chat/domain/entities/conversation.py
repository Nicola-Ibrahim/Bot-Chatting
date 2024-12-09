import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

from ....domain.primitive.entity import AggregateRoot, IDType
from ....domain.primitive.identifier import UUIDID
from ..value_objects.content import Content
from .message import Message


@dataclass
class Conversation(AggregateRoot):
    """
    Represents a conversation, handling multiple messages.
    """

    _id: IDType = field(default_factory=UUIDID.create)
    _messages: OrderedDict[uuid.UUID, Message] = field(default_factory=OrderedDict)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def start(cls):
        """Factory method to create a new conversation instance."""
        return cls()

    @property
    def messages(self):
        return self._messages

    @property
    def created_time(self):
        return self.timestamp

    def pin_message(self, message_id: uuid.UUID):
        """Pin a specific message for quick access."""
        message = self._check_message_exists(message_id)
        message.pinned = True

        # Raise the domain event
        event = MessagePinnedEvent(
            conversation_id=self._id,
            message_id=message_id,
            timestamp=str(datetime.now()),
        )
        self._record_event(event)

        return message

    def get_pinned_messages(self):
        """Retrieve all pinned messages."""
        return [message for message in self._messages.values() if getattr(message, "pinned", False)]

    def add_message(self, content: Content):
        """
        Adds a new message to the conversation.
        """

        # Create the message entity from the provided text and response
        message = Message.create(content=content)

        # Add the created message to the conversation
        self._messages[message.id] = message

        # Raise the domain event
        event = MessageAddedEvent(
            conversation_id=self._id,
            message_id=message.id,
            timestamp=str(datetime.now()),
        )

        self._record_event(event)

        return message

    def regenerate_or_edit_message(self, message_id: uuid.UUID, content: Content):
        """
        Regenerates or edits an existing message's content using the provided Content object.
        """
        message = self._check_message_exists(message_id)

        message.add_content(content)

        # Raise the domain event
        event = MessageEditedEvent(
            conversation_id=self._id,
            message_id=message_id,
            edited_content=content.text,
            timestamp=str(datetime.now()),
        )
        self._record_event(event)

        return content

    def get_last_n_messages(self, n: int):
        """
        Retrieves the last `n` messages in the conversation.
        """
        if n <= 0:
            raise ValueError("Number of messages must be positive.")  # Validation logic simplified
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

    def _check_message_exists(self, message_id: uuid.UUID):
        """
        Checks if a message with the given ID exists in the conversation.
        """
        if message_id not in self._messages:
            raise ValueError(f"Message with ID {message_id} not found.")
        return self._messages[message_id]
