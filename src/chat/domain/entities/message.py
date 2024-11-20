from dataclasses import dataclass, field

from src.shared.domain.entity import Entity

from ..exceptions import BusinessValidationException
from ..value_objects.content import Content, Feedback
from ..value_objects.feedback import Feedback


@dataclass
class Message(Entity):
    """Represents a series of messages and responses within a conversation."""

    _messages: list[Content] = field(default_factory=list)

    def __post_init__(self):
        """
        Enforces the business rule: An message must have at least one message.
        Raises a BusinessValidationException if no messages are provided.
        """
        if not self._messages:
            raise BusinessValidationException("An message must contain at least one message.")

    @property
    def all_messages(self) -> list[Content]:
        """Returns all messages in the message."""
        return self._messages

    @property
    def message_count(self) -> int:
        """Returns the total number of messages in the message."""
        return len(self._messages)

    @classmethod
    def create(cls, initial_message: Content) -> "Message":
        """
        Factory method to create a new Message instance.

        Args:
            initial_message (Content): The initial message to include in the message.

        Returns:
            Message: A new Message instance.
        """
        if not initial_message:
            raise BusinessValidationException("An initial message must be supplied when creating an message.")
        return cls(_messages=[initial_message])

    def add_message(self, message: Content) -> None:
        """
        Adds a new message to this message.

        Args:
            message (Content): The message to add.
        """
        self._messages.append(message)

    def get_latest_message(self) -> Content:
        """Returns the most recent message."""
        if self._messages:
            return self._messages[-1]
        raise BusinessValidationException("No messages available in the message.")

    def add_message_feedback(self, message_index: int, feedback: Feedback) -> None:
        """
        Adds feedback to a specific message within the message.

        Args:
            message_index (int): The index of the message to add feedback to.
            feedback (Feedback): The feedback object to add.

        Raises:
            BusinessValidationException: If the specified message index is invalid.
        """
        message = self._get_message_by_index(message_index)
        message.add_feedback(feedback)

    def update_message_feedback(self, message_index: int, feedback: Feedback) -> None:
        """
        Updates feedback for a specific message within the message.

        Args:
            message_index (int): The index of the message to update feedback for.
            feedback (Feedback): The new feedback object.

        Raises:
            BusinessValidationException: If the specified message index is invalid.
        """
        message = self._get_message_by_index(message_index)
        message.update_feedback(feedback)

    def _get_message_by_index(self, index: int) -> Content:
        """
        Retrieves a specific message by its index in the message.

        Args:
            index (int): The index of the message to retrieve.

        Returns:
            Content: The message at the specified index.

        Raises:
            BusinessValidationException: If the index is out of bounds.
        """
        if index < 0 or index >= len(self._messages):
            raise BusinessValidationException(f"Invalid message index: {index}")
        return self._messages[index]
