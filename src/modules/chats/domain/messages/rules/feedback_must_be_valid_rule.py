from dataclasses import dataclass

"""Business rule validating feedback structure.

Feedback is considered invalid when it lacks a rating or when a comment
exceeds 500 characters. The rule is broken when either of these
conditions holds true. Imports updated to correct package paths.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule
from src.modules.chats.domain.messages.value_objects.feedback import Feedback


@dataclass
class FeedbackMustBeValidRule(BaseBusinessRule):
    feedback: Feedback
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Feedback must have a valid rating and comment must be less than 500 characters."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        # Broken if rating is missing
        if self.feedback.rating is None:
            return True
        # Broken if comment exists and is too long
        if self.feedback.comment and len(self.feedback.comment) > 500:
            return True
        return False
