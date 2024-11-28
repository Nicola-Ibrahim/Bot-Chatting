from dataclasses import dataclass

from shared.infra.utils.result import Result
from src.shared.domain.value_object import ValueObject

from ..exceptions.operation import InValidOperationException
from .feedback import Feedback


@dataclass(frozen=True)
class Content(ValueObject):
    """Represents a user's question and the corresponding generated response."""

    text: str
    response: str
    feedback: Feedback | None = None

    def __post_init__(self):
        """Validates the message text and response text."""
        if not self.text or len(self.text) < 3:
            raise InValidOperationException("Content text must be at least 3 characters long.")
        if not self.response or len(self.response) < 3:
            raise InValidOperationException("Response text must be at least 3 characters long.")

    @classmethod
    def create(cls, text: str, response: str) -> Result:
        """Factory method to create content."""
        if not text or len(text) < 3:
            return Result.fail(InValidOperationException("Content text must be at least 3 characters long."))
        if not response or len(response) < 3:
            return Result.fail(InValidOperationException("Response text must be at least 3 characters long."))

        return Result.ok(cls(text=text, response=response))
