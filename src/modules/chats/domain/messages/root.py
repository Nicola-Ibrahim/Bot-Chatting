import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.building_blocks.domain.entity import AggregateRoot
from src.building_blocks.domain.exception import BusinessRuleValidationException

from ..conversations.value_objects.conversation_id import ConversationId
from ..members.value_objects.member_id import MemberId
from .events import MessageAddedEvent, MessageEditedEvent, MessagePinnedEvent, MessageUpdatedEvent
from .rules import (
    ContentResponseMustBeValidRule,
    ContentTextMustBeValidRule,
    ContentTextMustNotContainProfanityRule,
    FeedbackMustBeValidRule,
    NonEmptyMessageRule,
)
from .value_objects.content import Content
from .value_objects.feedback import Feedback
from .value_objects.message_id import MessageId


@dataclass
class Message(AggregateRoot):
    """
    Represents a message containing multiple contents and feedback.
    """

    _id: MessageId
    _conversation_id: ConversationId
    _sender_id: MemberId
    _contents: list[Content] = field(default_factory=list)
    _created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _pinned: bool = False

    @property
    def contents(self):
        return self._contents

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def pinned(self):
        return self._pinned

    @property
    def sender_id(self):
        return self._sender_id

    @classmethod
    def create(cls, conversation_id: uuid.UUID, sender_id: uuid.UUID, content: Content) -> "Message":
        """
        Factory method to create a new message instance.
        """
        instance = cls(_conversation_id=conversation_id, _sender_id=sender_id, _contents=[content])
        instance.add_event(MessageAddedEvent(conversation_id=conversation_id, message_id=instance._id))
        return instance

    def add_content(self, content: Content, conversation_id: uuid.UUID) -> Content:
        """
        Adds a new content version to the message and raises an event.
        """

        self.check_rule(ContentTextMustBeValidRule(text=content.text))
        self.check_rule(ContentResponseMustBeValidRule(response=content.response))
        self.check_rule(ContentTextMustNotContainProfanityRule(text=content.text))

        content = Content.create(content.text, content.response, content.feedback, conversation_id)
        self._contents.append(content)
        self._updated_at = datetime.now(timezone.utc)

        # Raise the domain event
        event = MessageUpdatedEvent(conversation_id=conversation_id, message_id=self._id)
        self.add_event(event)

        return content

    def update_message(self, content: Content):
        """
        Adds a new content version to the message and raises an event.
        """
        content = Content.create(content.text, content.response, content.feedback, self._conversation_id)
        self._contents.append(content)
        self.add_event(MessageUpdatedEvent(self.id, content))
        self._updated_at = datetime.now(timezone.utc)
        return content

    def get_latest_content(self):
        """
        Retrieves the most recent content of the message.
        """
        if not self._contents:
            raise BusinessRuleValidationException("No content available.")
        return self._contents[-1]

    def add_feedback(self, content_index: int, feedback: Feedback):
        """
        Adds feedback to a specific content by creating a new Content version.
        """

        self.check_rule(FeedbackMustBeValidRule(feedback=feedback))

        content = self._contents[content_index]
        updated_content = Content.create(content.text, content.response, feedback, self._conversation_id)
        self._contents[content_index] = updated_content
        return updated_content

    def regenerate_or_edit_message(self, message_id: uuid.UUID, content: Content):
        """
        Regenerates or edits an existing message's content using the provided Content object.
        """

        self.add_content(content)

        # Raise the domain event
        event = MessageEditedEvent(
            conversation_id=self._id,
            message_id=message_id,
            edited_content=content.text,
            timestamp=str(datetime.now(timezone.utc)),
        )
        self.add_event(event)

        return content

    def pin_message(self):
        """
        Pins the message.
        """
        self._pinned = True
        self.add_event(MessagePinnedEvent(conversation_id=self._conversation_id, message_id=self._id))

    def unpin_message(self):
        """
        Unpins the message.
        """
        self._pinned = False
        self.add_event(MessagePinnedEvent(conversation_id=self._conversation_id, message_id=self._id))

    def delete_content(self, content_id: uuid.UUID):
        """
        Deletes a specific content from the message.
        """
        self._contents = [content for content in self._contents if content.id != content_id]
        self.check_rule(NonEmptyMessageRule(self._contents))
        self._updated_at = datetime.now(timezone.utc)
        self.add_event(MessageUpdatedEvent(conversation_id=self._conversation_id, message_id=self._id))
