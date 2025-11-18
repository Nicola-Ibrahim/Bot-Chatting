from dataclasses import dataclass, field

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentTextMustBeValidRule(BaseBusinessRule):
    """Business rule validating that message text is non-empty and of minimum length.

    This rule is broken when the provided text is either empty or consists
    solely of whitespace. A valid message must contain at least one non-space
    character. Imports have been updated to reference the correct package.
    """

    text: str
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Content must be valid.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        # The rule is broken when the text is empty or contains only whitespace
        return not bool(self.text and self.text.strip())
