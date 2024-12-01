from dataclasses import dataclass
from typing import Optional

from ...infra.utils.result import Result
from ..enums.rating import RatingType
from .value_object import ValueObject


@dataclass(frozen=True)
class Feedback(ValueObject):
    """Represents feedback provided on a message."""

    rating: RatingType
    comment: Optional[str] = None

    def __post_init__(self):
        """Validates the business rules for feedback."""
        if self.comment and not self.comment.strip():
            raise ValueError("Comment cannot be an empty string.")

        if self.comment and len(self.comment) > 500:
            raise ValueError("Comment cannot exceed 500 characters.")

    @classmethod
    def create(cls, rating: RatingType, comment: Optional[str] = None) -> Result:
        """Factory method to create feedback."""
        if comment and len(comment) > 500:
            return Result.fail(ValueError("Comment cannot exceed 500 characters."))

        return Result.ok(cls(rating=rating, comment=comment))
