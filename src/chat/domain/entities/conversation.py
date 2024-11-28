import uuid
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime

from shared.infra.utils.result import Result
from src.shared.domain.entity import AggregateRoot

from ..exceptions.operation import InValidOperationException
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback
from ..value_objects.ids import ConversationId
from .message import Message


@dataclass
class Conversation(AggregateRoot):
    """
    Represents a chat session, handling multiple messages and responses.
    """

    _id: ConversationId = field(default=ConversationId.of(uuid.uuid4()))
    _messages: OrderedDict[uuid.UUID, Message] = field(default_factory=OrderedDict)
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def all_messages(self) -> Result:
        """Get all messages in the chat."""
        return Result.ok(list(self._messages.values()))

    @classmethod
    def create(cls) -> Result:
        """
        Factory method to create a new Conversation instance.

        Returns:
            Result: Success with a new, empty conversation instance.
        """
        return Result.ok(cls())

    @classmethod
    def from_existing(cls, conversation: "Conversation") -> Result:
        """
        Factory method to create a new Conversation instance based on an existing one.

        Args:
            conversation (Conversation): An existing conversation to load data from.

        Returns:
            Result: Success with the new conversation initialized with existing data.
        """
        # TODO: Apply domain rules and checks before returning the object
        return Result.ok(conversation)

    def add_message(self, message: Message) -> Result:

        self._messages[message.id] = message

        return message

    def regenerate_or_edit_message(self, message_id: uuid.UUID, text: str, response: str) -> Result:
        """
        Regenerates the response or updates the message text in the message.

        Args:
            message_id (uuid.UUID): The ID of the message to update.
            text (str): The new message text.
            response (str): The new generated response text.

        Returns:
            Result: Success or failure with an appropriate message.
        """
        check_result = self._check_message_exist(message_id)
        if check_result.is_failure():
            return check_result

        # Add the new content to the existing message
        content_result = Content.create(text=text, response=response)
        if content_result.is_failure():
            return content_result

        self._messages[message_id].add_message(content_result.value)
        return Result.ok(self._messages[message_id])

    def _check_message_exist(self, message_id: uuid.UUID) -> Result:
        """
        Checks if a message exists by its ID.

        Args:
            message_id (uuid.UUID): The ID of the message to check.

        Returns:
            Result: Success or failure with an error message.
        """
        if message_id not in self._messages:
            return Result.fail(InValidOperationException(f"Message with ID {message_id} not found."))
        return Result.ok(True)

    def get_last_n_messages(self, n: int) -> Result:
        """
        Retrieves the last `n` messages in the chat.

        Args:
            n (int): The number of recent messages to retrieve.

        Returns:
            Result: Success with the list of most recent `n` messages.
        """
        return Result.ok(list(self._messages.values())[-n:])

    def add_feedback_message(self, message_id: uuid.UUID, rating: str, comment: str = None) -> Result:
        """
        Adds feedback to a specific message.

        Args:
            message_id (uuid.UUID): The ID of the message to update.
            rating (str): The feedback rating.
            comment (str, optional): Additional comments for feedback.

        Returns:
            Result: Success or failure with an appropriate message.
        """
        check_result = self._check_message_exist(message_id)
        if check_result.is_failure():
            return check_result

        feedback = Feedback(rating=rating, comment=comment)
        self._messages[message_id].add_message_feedback(feedback)
        return Result.ok(True)

    def read_chat_partially(self, tokenizer, max_recent: int = 5, token_limit: int = 500) -> Result:
        """
        Retrieve recent messages from a chat, respecting a token limit.

        Args:
            tokenizer (AbstractTokenizerService): Tokenizer service to calculate tokens.
            max_recent (int): The maximum number of recent messages to retrieve.
            token_limit (int): The maximum token limit for the context.

        Returns:
            Result: Success with a list of recent messages within the token limit or failure.
        """
        last_messages = self.get_last_n_messages(max_recent).value

        selected_messages = []
        total_tokens = 0

        for message in reversed(last_messages):
            prompt_tokens = tokenizer.tokenize(message.text)
            response_tokens = tokenizer.tokenize(message.response.text if message.response else "")
            total = len(prompt_tokens) + len(response_tokens)

            if total_tokens + total > token_limit:
                break

            selected_messages.insert(0, message)
            total_tokens += total

        return Result.ok(selected_messages)
