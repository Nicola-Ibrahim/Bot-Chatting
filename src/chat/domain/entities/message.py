from dataclasses import dataclass, field
from datetime import datetime

from src.shared.domain.entity import Entity

from ....shared.domain.result import Result
from ..exceptions import InValidOperationException
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback


@dataclass
class Message(Entity):
    """Represents a series of contents and responses within a conversation."""

    timestamp: datetime = field(default_factory=datetime.now)

    _content: list[Content] = field(default_factory=list)

    # def __post_init__(self):
    #     """
    #     Enforces the business rule: An content must have at least one content.
    #     Raises a InValidOperationException if no contents are provided.
    #     """
    #     if not self._content:
    #         return Result(error=InValidOperationException("An content must contain at least one content."))

    @property
    def all_content(self) -> list[Content]:
        """Returns all contents ."""
        return self._content

    @property
    def content_count(self) -> int:
        """Returns the total number of contents ."""
        return len(self._content)

    @classmethod
    def create(cls, initial_content: Content) -> Result:
        """
        Factory method to create a new content instance.

        Args:
            initial_content (Content): The initial content to include .

        Returns:
            content: A new content instance.
        """
        if not initial_content:
            return Result.failure(
                InValidOperationException("An initial content must be supplied when creating an content.")
            )

        obj = super().__new__(cls)
        obj._content = [initial_content]  # Initialize the contents list

        obj = cls()
        obj._content.append(initial_content)

        return Result.success(value=obj)

    def add_content(self, content: Content) -> None:
        """
        Adds a new content to this content.

        Args:
            content (Content): The content to add.
        """
        self._content.append(content)

    def get_latest_content(self) -> Result:
        """Returns the most recent content."""
        if self._content:
            return Result.success(self._content[-1])
        return Result.failure(InValidOperationException("No contents available ."))

    def add_content_feedback(self, content_index: int, feedback: Feedback) -> None:
        """
        Adds feedback to a specific content with.

        Args:
            content_index (int): The index of the content to add feedback to.
            feedback (Feedback): The feedback object to add.

        Raises:
            InValidOperationException: If the specified content index is invalid.
        """
        content = self._get_content_by_index(content_index)
        content.add_feedback(feedback)

    def update_content_feedback(self, content_index: int, feedback: Feedback) -> None:
        """
        Updates feedback for a specific content with.

        Args:
            content_index (int): The index of the content to update feedback for.
            feedback (Feedback): The new feedback object.

        Raises:
            InValidOperationException: If the specified content index is invalid.
        """
        content = self._get_content_by_index(content_index)
        content.update_feedback(feedback)

    def _get_content_by_index(self, index: int) -> Result:
        """
        Retrieves a specific content by its index .

        Args:
            index (int): The index of the content to retrieve.

        Returns:
            Content: The content at the specified index.

        Raises:
            InValidOperationException: If the index is out of bounds.
        """
        if index < 0 or index >= len(self._content):
            return Result.failure(InValidOperationException(f"Invalid content index: {index}"))
        return Result.success(self._content[index])
