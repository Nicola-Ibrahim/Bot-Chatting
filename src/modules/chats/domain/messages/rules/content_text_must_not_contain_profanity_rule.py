from dataclasses import dataclass

"""Business rule ensuring a message does not contain profane words.

The rule is broken when any of the predefined profanities appear in the
text. Imports remain correct as they reference ``src.building_blocks``.
"""

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
        # The rule is broken if the text contains any profane word
        return any(profanity in self.text for profanity in profanities)
