from dataclasses import dataclass, field
from typing import Optional, Self

from src.building_blocks.domain.value_object import ValueObject

from ..enum.rating import RatingType
from ..rules import FeedbackMustBeValidRule


@dataclass(frozen=True, slots=True)
class Feedback(ValueObject):
    """Represents feedback provided on a message."""

    _rating: RatingType
    _comment: Optional[str] = None

    @property
    def rating(self) -> RatingType:
        return self._rating

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @classmethod
    def create(cls, rating: RatingType, comment: Optional[str] = None) -> Self:
        """
        Factory method to create feedback.

        Args:
            rating (RatingType): The rating given to the message.
            comment (Optional[str]): Optional comment providing additional feedback.

        Returns:
            Feedback: A new instance of the Feedback class.
        """
        cls.check_rules(FeedbackMustBeValidRule(rating=rating))
        return cls(_rating=rating, _comment=comment)
