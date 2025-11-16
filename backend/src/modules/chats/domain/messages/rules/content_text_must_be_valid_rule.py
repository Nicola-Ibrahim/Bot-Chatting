from dataclasses import dataclass

"""Business rule validating that message text is non-empty and of minimum length.

This rule is broken when the provided text is either empty or consists
solely of whitespace. A valid message must contain at least one non-space
character. Imports have been updated to reference the correct package.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(frozen=True)
class ContentTextMustBeValidRule(BaseBusinessRule):
    text: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Content must be valid."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        # The rule is broken when the text is empty or contains only whitespace
        return not bool(self.text and self.text.strip())
