from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule
from src.modules.chats.domain.messages.models.feedback import Feedback


@dataclass
class FeedbackMustBeValidRule(BaseBusinessRule):
    feedback: Feedback
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Feedback must have a valid rating and comment must be less than 500 characters."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_satisfied(self) -> bool:
        if not self.feedback.rating:
            return False
        if self.feedback.comment and len(self.feedback.comment) > 500:
            return False
        return True
