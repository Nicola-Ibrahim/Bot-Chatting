import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions.operation import InValidOperationException
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback
from ..value_objects.ids import UUIDID
from .entity import AggregateRoot, IDType
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
        """
        Factory method to create a new conversation instance.
        """
        return cls()

    @property
    def messages(self):
        return self._messages

    @property
    def created_time(self):
        return self.timestamp

    def add_message(self, content: Content):
        """
        Adds a new message to the conversation.
        Handles creation of the Message entity and ensures that the
        text and response are valid before adding it.
        """
        # Validate the text and response
        if not content.text or len(content.text) < 3:
            raise InValidOperationException.validation("Message text must be at least 3 characters long.")

        if not content.response or len(content.response) < 3:
            raise InValidOperationException.validation("Response text must be at least 3 characters long.")

        # Create the message entity from the provided text and response
        message = Message.create(content)

        # Add the created message to the conversation
        self._messages[message.id] = message
        return message

    def regenerate_or_edit_message(self, message_id: uuid.UUID, content: Content):
        """
        Regenerates or edits an existing message's content using the provided Content object.
        """
        # First, check if the message exists
        message = self._check_message_exists(message_id)

        # Validate the provided content
        if content.is_invalid():
            raise InValidOperationException.validation("Message text and response must be at least 3 characters long.")

        # Retrieve the message and update its content
        return message.add_content(content)

    def _check_message_exists(self, message_id: uuid.UUID):
        """
        Checks if a message with the given ID exists in the conversation.
        """
        if message_id not in self._messages:
            raise InValidOperationException.not_found(f"Message with ID {message_id} not found.")
        return self._messages[message_id]

    def get_last_n_messages(self, n: int):
        """
        Retrieves the last `n` messages in the conversation.
        """
        if n <= 0:
            raise InValidOperationException.validation("Number of messages must be positive.")
        return list(self._messages.values())[-n:]

    def add_feedback_message(self, message_id: uuid.UUID, content_pos: int, feedback: Feedback):
        """
        Adds feedback to a specific message in the conversation.
        """
        message = self._check_message_exists(message_id)
        return message.add_content_feedback(content_pos, feedback)

    def read_chat_partially(self, tokenizer, max_recent: int = 5, token_limit: int = 500):
        """
        Retrieves recent messages from the conversation within a token limit.
        """
        last_messages = self.get_last_n_messages(max_recent)
        selected_messages = []
        total_tokens = 0

        for message in reversed(last_messages):
            prompt_tokens = tokenizer.tokenize(message.text)
            response_tokens = tokenizer.tokenize(message.response.text if message.response else "")
            total = len(prompt_tokens) + len(response_tokens)

            if total_tokens + total > token_limit:
                break

            selected_messages.insert(0, message)
            total_tokens += total

        return selected_messages
