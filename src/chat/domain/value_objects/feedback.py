from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RatingType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"


@dataclass(frozen=True)
class Feedback:
    """
    Value object representing feedback provided on an message or message.
    """

    rating: RatingType
    comment: Optional[str] = None

    def __post_init__(self):
        """
        Validates the business rules for feedback.
        """
        # Ensure comments are non-empty if provided
        if self.comment and not self.comment.strip():
            raise ValueError("Comment cannot be an empty string.")

        # Enforce length constraints for comments
        if self.comment and len(self.comment) > 500:
            raise ValueError("Comment cannot exceed 500 characters.")

    @classmethod
    def create(cls) -> 'Feedback':
        """
        Creates a new Feedback instance with updated values (immutability preserved).

        Args:
            rating (RatingType): The updated feedback type.
            comment (Optional[str]): The updated comment.

        Returns:
            Feedback: A new Feedback instance with updated values.
        """
        return cls(type=rating, comment=comment)
