from dataclasses import dataclass
from typing import Optional

from ....domain.primitive.value_object import ValueObject
from ..messages.rating import RatingType
from ..exceptions.operation import InValidOperationException


@dataclass(frozen=True)
class Feedback(ValueObject):
    """Represents feedback provided on a message."""

    _rating: RatingType
    _comment: Optional[str] = None

    @property
    def rating(self):
        return self._rating

    @property
    def comment(self):
        return self._comment

    def validate(self) -> bool:
        """
        Validates the business rules for feedback.

        Returns:
            bool: True if valid, raises an exception otherwise.
        """
        # Validate rating
        if not isinstance(self._rating, RatingType):
            raise InValidOperationException.validation(
                "Invalid rating type provided. Must be a valid RatingType enum."
            )

        # Validate comment
        if self._comment is not None:
            trimmed_comment = self._comment.strip()
            if not trimmed_comment:
                raise InValidOperationException.validation("Comment cannot be empty or whitespace.")
            if len(trimmed_comment) > 500:
                raise InValidOperationException.validation("Comment cannot exceed 500 characters.")

        return True

    @classmethod
    def create(cls, rating: RatingType, comment: Optional[str] = None) -> "Feedback":
        """Factory method to create feedback."""
        return cls(_rating=rating, _comment=comment)
