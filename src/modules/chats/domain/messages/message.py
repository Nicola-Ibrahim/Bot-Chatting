import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.entity import AggregateRoot

from .content import Content
from .events.message import MessageUpdatedEvent
from .feedback import Feedback


@dataclass
class Message(AggregateRoot):
    """
    Represents a message containing multiple contents and feedback.
    """

    _contents: list[Content] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def contents(self):
        return self._contents

    @classmethod
    def create(cls, content: Content):
        """
        Factory method to create a new message instance.
        """
        if not content:
            raise InValidOperationException.validation("Initial content must be provided.")

        return cls(_contents=[content])

    def add_content(self, content: Content, conversation_id: uuid.UUID):
        """
        Adds a new content version to the message and raises an event.
        """
        if not content:
            raise InValidOperationException.validation("Content cannot be null.")
        self._contents.append(content)

        event = MessageUpdatedEvent(
            conversation_id=conversation_id,
            message_id=self._id,
            content_id=content.id,
        )
        self._record_event(event)

    def update_message(self, content: Content):
        """
        Adds a new content to the message.
        """
        if not content:
            raise InValidOperationException.validation("Content cannot be null.")

        self._contents.append(content)
        return content

    def get_latest_content(self):
        """
        Retrieves the most recent content of the message.
        """
        if not self._contents:
            raise InValidOperationException.validation("No content available.")
        return self._contents[-1]

    def add_feedback(self, content_index: int, feedback: Feedback):
        """
        Adds feedback to a specific content by creating a new Content version.
        """
        if content_index < 0 or content_index >= len(self._contents):
            raise ValueError("Invalid content index.")
        content = self._contents[content_index]
        updated_content = Content.create(content.text, content.response, feedback)
        self._contents[content_index] = updated_content
        return updated_content
