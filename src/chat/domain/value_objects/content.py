from dataclasses import dataclass
from typing import Optional

from ..exceptions.operation import InValidOperationException
from .feedback import Feedback
from .value_object import ValueObject


@dataclass(frozen=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    text: str
    response: str
    feedback: Optional[Feedback] = None

    def validate(self) -> bool:
        """
        Validates the business rules for content.

        Returns:
            bool: True if valid, raises an exception otherwise.
        """
        if not self.text or len(self.text) < 3:
            raise InValidOperationException.validation("Content text must be at least 3 characters long.")
        if not self.response or len(self.response) < 3:
            raise InValidOperationException.validation("Response text must be at least 3 characters long.")
        return True

    @classmethod
    def create(cls, text: str, response: str) -> "Content":
        """
        Factory method to create a content instance with validation.

        Args:
            text (str): The content text (question).
            response (str): The generated response text.

        Returns:
            Content: A new `Content` object if valid, otherwise raises an exception.
        """
        content = cls(text=text, response=response)
        content.validate()
        return content

    @classmethod
    def with_feedback(cls, text: str, response: str, feedback: Feedback) -> "Content":
        """
        Creates a new `Content` object with the provided feedback.

        Args:
            text (str): The content text (question).
            response (str): The generated response text.
            feedback (Feedback): The feedback for the content.

        Returns:
            Content: A new `Content` object with the added feedback if valid.
        """
        content = cls(text=text, response=response, feedback=feedback)
        content.validate()
        return content
