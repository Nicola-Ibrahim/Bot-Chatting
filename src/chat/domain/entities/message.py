import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain.entity import Entity

from ....shared.infra.utils.result import Result
from ..exceptions.operation import InValidOperationException
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback
from ..value_objects.ids import MessageId


@dataclass
class Message(Entity):
    """Represents a series of contents and responses within a conversation."""

    _id: MessageId = field(default=MessageId.of(uuid.uuid4()))
    _contents: list[Content] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def all_contents(self) -> list[Content]:
        """Returns all contents."""
        return self._contents

    @property
    def content_count(self) -> int:
        """Returns the total number of contents."""
        return len(self._contents)

    @classmethod
    def create(cls, contents: list[Content]) -> Result:
        """
        Factory method to create a new message instance with an initial content.

        Args:
            content (Content): The initial content to include.

        Returns:
            Result: Success with the new Message instance or failure with an error.
        """
        if not contents:
            return Result.fail(
                InValidOperationException("An initial content must be supplied when creating a message.")
            )

        obj = cls(_contents=contents)
        return Result.ok(obj)

    def add_content(self, content: Content) -> Result:
        """
        Adds a new content to this message.

        Args:
            content (Content): The content to add.

        Returns:
            Result: Success or failure of adding content.
        """
        if not content:
            return Result.fail(InValidOperationException("Content cannot be null or empty."))

        self._contents.append(content)
        return Result.ok(self)

    def get_latest_content(self) -> Result:
        """Returns the most recent content."""
        if self._contents:
            return Result.ok(self._contents[-1])
        return Result.fail(InValidOperationException("No contents available."))

    def add_content_feedback(self, content_index: int, feedback: Feedback) -> Result:
        """
        Adds feedback to a specific content.

        Args:
            content_index (int): The index of the content to add feedback to.
            feedback (Feedback): The feedback object to add.

        Returns:
            Result: Success or failure with an error message.
        """
        content_result = self._get_content_by_index(content_index)
        if content_result.is_failure():
            return content_result

        content_result.value.add_feedback(feedback)
        return Result.ok(content_result.value)

    def update_content_feedback(self, content_index: int, feedback: Feedback) -> Result:
        """
        Updates feedback for a specific content.

        Args:
            content_index (int): The index of the content to update feedback for.
            feedback (Feedback): The new feedback object.

        Returns:
            Result: Success or failure with an error message.
        """
        content_result = self._get_content_by_index(content_index)
        if content_result.is_failure():
            return content_result

        content_result.value.update_feedback(feedback)
        return Result.ok(content_result.value)

    def _get_content_by_index(self, index: int) -> Result:
        """
        Retrieves a specific content by its index.

        Args:
            index (int): The index of the content to retrieve.

        Returns:
            Result: Success with the content or failure if index is out of bounds.
        """
        if index < 0 or index >= len(self._contents):
            return Result.fail(InValidOperationException(f"Invalid content index: {index}"))
        return Result.ok(self._contents[index])
