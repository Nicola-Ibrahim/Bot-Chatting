from dataclasses import dataclass
from typing import Optional

from ...infra.utils.result import Result
from ..exceptions.operation import InValidOperationException
from .feedback import Feedback
from .value_object import ValueObject


@dataclass(frozen=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    text: str
    response: str
    feedback: Optional[Feedback] = None

    @classmethod
    def create(cls, text: str, response: str) -> Result["Content", InValidOperationException]:
        """
        Factory method to create a content instance with validation.

        Args:
            text (str): The content text (question).
            response (str): The generated response text.

        Returns:
            Result: Success with the created `Content` or failure with an error message.
        """
        # Validate the text and response lengths
        if not text or len(text) < 3:
            return Result.fail(InValidOperationException("Content text must be at least 3 characters long."))
        if not response or len(response) < 3:
            return Result.fail(InValidOperationException("Response text must be at least 3 characters long."))

        # Return the result with a valid Content object
        return Result.ok(cls(text=text, response=response))

    @classmethod
    def with_feedback(cls, text: str, response: str, feedback: Feedback) -> "Content":
        """
        Creates a new Content object with the provided feedback.

        Args:
            feedback (Feedback): The feedback for the content.

        Returns:
            Content: A new `Content` object with the added feedback.
        """
        # Validate the text and response lengths
        if not text or len(text) < 3:
            return Result.fail(InValidOperationException("Content text must be at least 3 characters long."))
        if not response or len(response) < 3:
            return Result.fail(InValidOperationException("Response text must be at least 3 characters long."))

        return Result.ok(cls(text=text, response=response, feedback=feedback))
