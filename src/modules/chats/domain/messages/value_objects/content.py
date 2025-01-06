from dataclasses import dataclass

from src.building_blocks.domain.value_object import ValueObject

from .feedback import Feedback


@dataclass(frozen=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    _text: str
    _response: str
    _feedback: Feedback | None = None

    @property
    def text(self):
        return self._text

    @property
    def response(self):
        return self._response

    @property
    def feedback(self):
        return self._feedback

    @classmethod
    def create(cls, text: str, response: str, feedback: Feedback = None) -> "Content":
        """
        Factory method to create a content instance with validation.
        """
        return cls(_text=text, _response=response, _feedback=feedback)
