from dataclasses import dataclass
from typing import Optional

from ..enums.rating import RatingType
from ..exceptions.operation import InValidOperationException
from .value_object import ValueObject


@dataclass(frozen=True)
class Feedback(ValueObject):
    """Represents feedback provided on a message."""

    rating: RatingType
    comment: Optional[str] = None

    def validate(self) -> bool:
        """
        Validates the business rules for feedback.

        Returns:
            bool: True if valid, raises an exception otherwise.
        """
        if self.comment and not self.comment.strip():
            raise InValidOperationException.validation("Comment cannot be an empty string.")

        if self.comment and len(self.comment) > 500:
            raise InValidOperationException.validation("Comment cannot exceed 500 characters.")

        return True

    @classmethod
    def create(cls, rating: RatingType, comment: Optional[str] = None) -> "Feedback":
        """Factory method to create feedback."""
        feedback = cls(rating=rating, comment=comment)
        feedback.validate()  # Validate the feedback upon creation
        return feedback
