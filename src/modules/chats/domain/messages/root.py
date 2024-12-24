import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.building_blocks.domain.entity import AggregateRoot
from src.building_blocks.domain.exception import BusinessRuleValidationException

from .events.message_pinned import MessageUpdatedEvent
from .models.content import Content
from .models.feedback import Feedback
from .rules import (ContentIndexMustBeValidRule,
                    ContentMustBelongToConversationRule,
                    InitialContentMustBeProvidedRule, MessageMustExistRule)


@dataclass
class Message(AggregateRoot):
    """
    Represents a message containing multiple contents and feedback.
    """

    _conversation_id: uuid.UUID
    _contents: list[Content] = field(default_factory=list)

    @property
    def contents(self):
        return self._contents

    @classmethod
    def create(cls, conversation_id: uuid.UUID, content: Content) -> "Message":
        """
        Factory method to create a new message instance.
        """
        instance = cls(_conversation_id=conversation_id, _contents=[content])
        instance.check_rule(InitialContentMustBeProvidedRule(content))
        return instance

    def add_content(self, content: Content, conversation_id: uuid.UUID) -> Content:
        """
        Adds a new content version to the message and raises an event.
        """
        self.check_rule(ContentMustBelongToConversationRule(content, conversation_id))
        self._contents.append(content)

        # Raise the domain event
        event = MessageUpdatedEvent(
            conversation_id=conversation_id,
            message_id=self._id,
            content_id=content.id,
        )
        self.add_event(event)

        return content


    def update_message(self, content: Content):
        """
        Adds a new content version to the message and raises an event.
        """
        self.check_rule(ContentMustBelongToConversationRule(content, conversation_id))
        self._contents.append(content)
        self.raise_event(MessageUpdatedEvent(self.id, content))
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
        self.check_rule(ContentIndexMustBeValidRule(content_index, len(self._contents)))
        content = self._contents[content_index]
        updated_content = Content.create(content.text, content.response, feedback)
        self._contents[content_index] = updated_content
        return updated_content

    def regenerate_or_edit_message(self, message_id: uuid.UUID, content: Content):
        """
        Regenerates or edits an existing message's content using the provided Content object.
        """
        message = self._check_message_exists(message_id)
        self.check_rule(MessageMustExistRule(message))

        message.add_content(content)

        # Raise the domain event
        event = MessageEditedEvent(
            conversation_id=self._id,
            message_id=message_id,
            edited_content=content.text,
            timestamp=str(datetime.now()),
        )
        self.add_event(event)

        return content
        )
        self.add_event(event)

        return content
