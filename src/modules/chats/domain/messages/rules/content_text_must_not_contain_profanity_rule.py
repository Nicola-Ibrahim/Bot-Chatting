from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(frozen=True)
class ContentTextMustNotContainProfanityRule(BaseBusinessRule):
    text: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Content must not contain profanity."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        profanities = ["badword1", "badword2"]
        return not any(profanity in self.text for profanity in profanities)
