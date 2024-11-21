from dataclasses import dataclass, field

from src.shared.domain.entity import Entity

from ..exceptions import InValidOperationException
from ..result_model import Result
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback


@dataclass
class Message(Entity):
    """Represents a series of messages and responses within a conversation."""

    _messages: list[Content] = field(default_factory=list)

    # def __post_init__(self):
    #     """
    #     Enforces the business rule: An message must have at least one message.
    #     Raises a InValidOperationException if no messages are provided.
    #     """
    #     if not self._messages:
    #         return Result(error=InValidOperationException("An message must contain at least one message."))

    @property
    def all_messages(self) -> list[Content]:
        """Returns all messages in the message."""
        return self._messages

    @property
    def message_count(self) -> int:
        """Returns the total number of messages in the message."""
        return len(self._messages)

    @classmethod
    def create(cls, initial_message: Content) -> Result:
        """
        Factory method to create a new Message instance.

        Args:
            initial_message (Content): The initial message to include in the message.

        Returns:
            Message: A new Message instance.
        """
        if not initial_message:
            return Result.failure(
                InValidOperationException("An initial message must be supplied when creating an message.")
            )

        obj = super().__new__(cls)
        obj._messages = [initial_message]  # Initialize the messages list

        return Result.success(obj)

    def add_message(self, message: Content) -> None:
        """
        Adds a new message to this message.

        Args:
            message (Content): The message to add.
        """
        self._messages.append(message)

    def get_latest_message(self) -> Result:
        """Returns the most recent message."""
        if self._messages:
            return Result.success(self._messages[-1])
        return Result.failure(InValidOperationException("No messages available in the message."))

    def add_message_feedback(self, message_index: int, feedback: Feedback) -> None:
        """
        Adds feedback to a specific message within the message.

        Args:
            message_index (int): The index of the message to add feedback to.
            feedback (Feedback): The feedback object to add.

        Raises:
            InValidOperationException: If the specified message index is invalid.
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
            InValidOperationException: If the specified message index is invalid.
        """
        message = self._get_message_by_index(message_index)
        message.update_feedback(feedback)

    def _get_message_by_index(self, index: int) -> Result:
        """
        Retrieves a specific message by its index in the message.

        Args:
            index (int): The index of the message to retrieve.

        Returns:
            Content: The message at the specified index.

        Raises:
            InValidOperationException: If the index is out of bounds.
        """
        if index < 0 or index >= len(self._messages):
            return Result.failure(InValidOperationException(f"Invalid message index: {index}"))
        return Result.success(self._messages[index])
