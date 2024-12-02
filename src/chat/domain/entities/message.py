from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions.operation import InValidOperationException
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback
from ..value_objects.ids import UUIDID
from .entity import Entity, IDType


@dataclass
class Message(Entity):
    """
    Represents a message containing multiple contents.
    """

    _id: IDType = field(default_factory=UUIDID.create)
    _contents: list[Content] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, content: Content):
        """
        Factory method to create a new message instance.
        """
        if not content:
            raise InValidOperationException.validation("Initial content must be provided.")

        return cls(_contents=[content])

    def add_content(self, content: Content):
        """
        Adds a new content to the message.
        """
        if not content:
            raise InValidOperationException.validation("Content cannot be null.")

        self._contents.append(content)
        return self

    def get_latest_content(self):
        """
        Retrieves the most recent content in the message.
        """
        if not self._contents:
            raise InValidOperationException.validation("No content available.")
        return self._contents[-1]

    def add_content_feedback(self, content_index: int, feedback: Feedback):
        """
        Adds feedback to a specific content by creating a new Content instance
        with the updated feedback and replacing the old content.
        """
        content = self._get_content_by_index(content_index)

        # Create a new Content with feedback
        new_content = Content.with_feedback(content.text, content.response, feedback)

        # Replace the old content with the new one
        self._contents[content_index] = new_content
        return new_content

    def _get_content_by_index(self, index: int):
        """
        Retrieves a specific content by its index.
        """
        if index < 0 or index >= len(self._contents):
            raise InValidOperationException.validation(f"Invalid content index: {index}")
        return self._contents[index]
