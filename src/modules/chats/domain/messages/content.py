from dataclasses import dataclass
from typing import Optional

from src.building_blocks.domain.value_object import ValueObject

from ..exceptions.operation import InValidOperationException
from .feedback import Feedback


@dataclass(frozen=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    _text: str
    _response: str
    _feedback: Optional[Feedback] = None

    @property
    def text(self):
        return self._text

    @property
    def response(self):
        return self._response

    @property
    def feedback(self):
        return self._feedback

    def validate(self) -> bool:
        """
        Validates the business rules for content.

        Returns:
            bool: True if valid, raises an exception otherwise.
        """
        if not self._text or len(self._text) < 3:
            raise InValidOperationException.validation("Content text must be at least 3 characters long.")
        if not self._response or len(self._response) < 3:
            raise InValidOperationException.validation("Response text must be at least 3 characters long.")
        return True

    @classmethod
    def create(cls, text: str, response: str, feedback: Feedback = None) -> "Content":
        """
        Factory method to create a content instance with validation.

        Args:
            text (str): The content text (question).
            response (str): The generated response text.

        Returns:
            Content: A new `Content` object if valid, otherwise raises an exception.
        """

        cls.check_rule(ContentCreateRule)
        return cls(_text=text, _response=response, _feedback=feedback)
