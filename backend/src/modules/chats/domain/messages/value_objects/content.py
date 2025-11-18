from dataclasses import dataclass, field
from typing import Optional, Self

from src.building_blocks.domain.value_object import ValueObject

from ..rules import ContentResponseMustBeValidRule, ContentTextMustBeValidRule, ContentTextMustNotContainProfanityRule
from .feedback import Feedback


@dataclass(slots=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    _text: str
    _response: str
    _feedback: Optional[Feedback] = None

    @property
    def text(self) -> str:
        return self._text

    @property
    def response(self) -> str:
        return self._response

    @property
    def feedback(self) -> Optional[Feedback]:
        return self._feedback

    @classmethod
    def create(cls, text: str, response: str, feedback: Optional[Feedback] = None) -> Self:
        """
        Factory method to create a content instance with validation.

        Args:
            text (str): The user's question or input.
            response (str): The corresponding generated response.
            feedback (Optional[Feedback]): Feedback provided on the message.

        Returns:
            Content: A new instance of the Content class.
        """
        cls.check_rules(
            ContentTextMustBeValidRule(text=text),
            ContentResponseMustBeValidRule(response=response),
            ContentTextMustNotContainProfanityRule(text=text),
        )
        return cls(_text=text, _response=response, _feedback=feedback)
