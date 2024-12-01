from dataclasses import dataclass, field
from datetime import datetime

from ...infra.utils.result import Result
from ..exceptions.operation import InValidOperationException

# Domain-specific imports
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback


@dataclass
class Message:
    """
    Represents a message containing multiple contents.
    """

    _contents: list[Content] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(content: Content) -> Result:
        """
        Factory method to create a new message instance.
        """
        if not content:
            return Result.fail(InValidOperationException("Initial content must be provided."))

        return Result.ok(Message(_contents=[content]))

    def add_content(self, content: Content) -> Result:
        """
        Adds a new content to the message.
        """
        if not content:
            return Result.fail(InValidOperationException("Content cannot be null."))

        self._contents.append(content)
        return Result.ok(self)

    def get_latest_content(self) -> Result:
        """
        Retrieves the most recent content in the message.
        """
        if not self._contents:
            return Result.fail(InValidOperationException("No content available."))

        return Result.ok(self._contents[-1])

    def add_content_feedback(self, content_index: int, feedback: Feedback) -> Result:
        """
        Adds feedback to a specific content by creating a new Content instance
        with the updated feedback and replacing the old content.
        """
        content_result = self._get_content_by_index(content_index)
        if content_result.is_failure():
            return content_result

        # Create a new Content with feedback
        content = content_result.value
        new_content_result = Content.with_feedback(content.text, content.response, feedback)
        if new_content_result.is_failure():
            return new_content_result

        # Replace the old content with the new one
        self._contents[content_index] = new_content_result.value
        return Result.ok(new_content_result.value)

    def _get_content_by_index(self, index: int) -> Result:
        """
        Retrieves a specific content by its index.
        """
        if index < 0 or index >= len(self._contents):
            return Result.fail(InValidOperationException(f"Invalid content index: {index}"))
        return Result.ok(self._contents[index])
