from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import InValidOperationException
from .feedback import Feedback


@dataclass(frozen=True)
class Content:
    """Represents a user's question and the corresponding generated response."""

    text: str
    response: str
    timestamp: datetime = field(default_factory=datetime.now)
    feedback: Feedback | None = None

    def __post_init__(self):
        """Validates the message text and response text."""
        if not self.text or len(self.text) < 3:
            raise InValidOperationException("Content text must be at least 3 characters long.")
        if not self.response or len(self.response) < 3:
            raise InValidOperationException("Response text must be at least 3 characters long.")

    def __str__(self) -> str:
        return f"Content: {self.text}\nResponse: {self.response}"

    @classmethod
    def create(cls, text: str, response: str):
        return cls(text=text, response=response)
