from dataclasses import dataclass
from typing import Optional

from src.building_blocks.domain.value_object import ValueObject

from .rating import RatingType


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

    @classmethod
    def create(cls, rating: RatingType, comment: Optional[str] = None) -> "Feedback":
        """Factory method to create feedback."""
        return cls(_rating=rating, _comment=comment)
