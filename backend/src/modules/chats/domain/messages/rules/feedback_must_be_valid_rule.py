from dataclasses import dataclass, field
from typing import Optional

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule
from src.modules.chats.domain.messages.enum.rating import RatingType


@dataclass
class FeedbackMustBeValidRule(BaseBusinessRule):
    """Business rule validating feedback structure."""

    rating: RatingType | None
    comment: Optional[str] = None
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Feedback must have a valid rating and comment must be less than 500 characters.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        if self.rating is None:
            return True
        if self.comment and len(self.comment) > 500:
            return True
        return False
