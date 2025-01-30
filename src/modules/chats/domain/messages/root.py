import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Self

from src.building_blocks.domain.entity import AggregateRoot
from src.building_blocks.domain.exception import BusinessRuleValidationException

from ..conversations.value_objects.conversation_id import ConversationId
from ..members.value_objects.member_id import MemberId
from .events import (
    MessageContentUpdatedEvent,
    MessageCreatedEvent,
    MessageEditedEvent,
    MessagePinnedEvent,
    MessageUpdatedEvent,
)
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


@dataclass(kw_only=True)
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
    _version: int = 0

    @property
    def contents(self) -> list[Content]:
        return self._contents

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def pinned(self) -> bool:
        return self._pinned

    @property
    def sender_id(self) -> MemberId:
        return self._sender_id

    @classmethod
    def create(
        cls,
        message_id: MessageId,
        conversation_id: ConversationId,
        sender_id: MemberId,
        content: Content,
    ) -> Self:
        """
        Factory method to create a new message instance.

        Args:
            conversation_id (ConversationId): The ID of the conversation.
            sender_id (MemberId): The ID of the sender.
            content (Content): The content of the message.

        Returns:
            Message: The newly created message.
        """
        # Create the message
        message = cls(
            _id=message_id,
            _conversation_id=conversation_id,
            _sender_id=sender_id,
        )
        message._contents.append(content)

        # Emit a domain event
        message.add_event(
            MessageCreatedEvent(
                message_id=message._id.value,
                conversation_id=conversation_id.value,
                sender_id=sender_id.value,
                text=content.text,
                response=content.response,
            )
        )

        return message

    def append_content(self, content: Content, conversation_id: uuid.UUID) -> Content:
        """
        Appends a new content version to the message and raises an event.
        """
        self.validate_content(content)
        updated_content = Content.create(text=content.text, response=content.response, feedback=content.feedback)
        self._contents.append(updated_content)
        self._updated_at = datetime.now(timezone.utc)
        self._version += 1
        self.add_event(MessageContentUpdatedEvent(conversation_id=conversation_id, message_id=self._id.value))
        return updated_content

    def validate_content(self, content: Content):
        """
        Validates the content against various business rules.
        """
        self.check_rules(
            ContentTextMustBeValidRule(text=content.text),
            ContentResponseMustBeValidRule(response=content.response),
            ContentTextMustNotContainProfanityRule(text=content.text),
        )

    def add_feedback(self, content_index: int, feedback: Feedback) -> Content:
        """
        Adds feedback to a specific content by creating a new Content version.
        """
        self.check_rules(FeedbackMustBeValidRule(feedback=feedback))
        content = self._contents[content_index]
        updated_content = Content.create(
            text=content.text,
            response=content.response,
            feedback=feedback,
        )
        self._contents[content_index] = updated_content
        self._version += 1
        return updated_content

    def pin_message(self) -> None:
        """
        Pins the message.
        """
        self._pinned = True
        self.add_event(MessagePinnedEvent(conversation_id=self._conversation_id.value, message_id=self._id.value))

    def unpin_message(self) -> None:
        """
        Unpins the message.
        """
        self._pinned = False
        self.add_event(MessagePinnedEvent(conversation_id=self._conversation_id.value, message_id=self._id.value))

    def get_latest_content(self) -> Content:
        """
        Retrieves the most recent content of the message.
        """
        if not self._contents:
            raise BusinessRuleValidationException("No content available.")
        return self._contents[-1]

    def delete_content(self, content_id: uuid.UUID) -> None:
        """
        Deletes a specific content from the message.
        """
        self._contents = [content for content in self._contents if content.id != content_id]
        if not self._contents:
            raise BusinessRuleValidationException("Message must have at least one content.")
        self._updated_at = datetime.now(timezone.utc)
        self.add_event(
            MessageContentUpdatedEvent(conversation_id=self._conversation_id.value, message_id=self._id.value)
        )
