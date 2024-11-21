import uuid
from collections import OrderedDict
from dataclasses import dataclass, field

from src.shared.domain.entity import AggregateRoot

from ..exceptions import InValidOperationException
from ..result_model import Result
from ..value_objects.content import Content
from ..value_objects.feedback import Feedback
from .message import Message


@dataclass
class Conversation(AggregateRoot):
    """
    Represents a chat session, handling multiple messages and responses.
    """

    _messages: OrderedDict[uuid.UUID, Message] = field(default_factory=OrderedDict)

    @property
    def all_messages(self) -> list[Message]:
        """Get all messages in the chat."""
        return list(self._messages.values())

    @classmethod
    def create(cls) -> "Conversation":
        """
        Factory method to create a new Conversation instance.

        Returns:
            Conversation: A new, empty conversation instance.
        """
        obj = super().__new__(cls)  # Bypass `__init__`

        return Result.success(obj)

    def add_message(self, text: str, response: str) -> None:
        """
        Creates a new message (message + response), adds it to the session.

        Args:
            message_text (str): The content of the user's message.
            response_text (str): The content of the generated response.
        """
        message = Content(text=text, response=response)
        message = Message.create(initial_message=message)
        message.add_message(message=message)
        self._messages[message.id] = message

    def format(self):
        """format a response in specific formatting"""
        pass

    def regenerate_or_edit_message(self, message_id: uuid.UUID, text: str, response: str) -> None:
        """
        Regenerates the response or updates the message text in the message.

        Args:
            message_id (uuid.UUID): The ID of the message to update.
            text (str): The new message (question) text.
            response (str): The new generated response text.

        Raises:
            InValidOperationException: If the message ID is invalid.
        """
        message = self._check_message_by_id(message_id)

        # Add the new message and response as a new Content object
        new_message = Content(text=text, response=response)
        self._messages[message_id].add_message(new_message)

    def _check_message_exist(self, message_id: uuid.UUID) -> bool:
        """
        Finds an message by its ID.

        Args:
            message_id (uuid.UUID): The ID of the message to find.

        Returns:
            Message: The matching message.

        Raises:
            InValidOperationException: If the message is not found.
        """
        message = self._messages.get(message_id)
        if not message:
            raise InValidOperationException(f"Message with ID {message_id} not found.")
        return True

    def get_last_n_messages(self, n: int) -> list[Message]:
        """
        Retrieves the last `n` messages in the chat.

        Args:
            n (int): The number of recent messages to retrieve.

        Returns:
            list[Message]: The most recent `n` messages.
        """
        return list(self._messages.values())[-n:]

    def add_feedback_message(self, message_id: uuid.UUID, rating: str, comment: str = None):
        feedback = Feedback(rating=rating, comment=comment)

        self._check_message_exist(message_id=message_id)

        self._messages[message_id].add_message_feedback(feedback=feedback)

    def update_feedback_message(self, message_id: uuid.UUID, message_num: str, rating: str, comment: str = None):

        self._check_message_exist(message_id=message_id)

        self._messages[message_id].update_message_feedback(message_num=message_num, feedback=feedback)

    def read_chat_partially(
        self, tokenizer: AbstractTokenizerService, max_recent: int = 5, token_limit: int = 500
    ) -> list[Content]:
        """
        Retrieve recent messages from a chat, respecting a token limit.

        Args:
            chat_id (uuid.UUID): The ID of the chat.
            max_recent (int): The maximum number of recent messages to retrieve.
            token_limit (int): The maximum token limit for the context.

        Returns:
            list[Content]: A list of recent messages within the token limit.

        Raises:
            InValidOperationException: If the chat does not exist.
        """

        # Retrieve recent messages
        last_messages = chat.get_last_n_messages(max_recent)

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

        return selected_messages
