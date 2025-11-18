from dataclasses import dataclass, field

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class NonEmptyMessageRule(BaseBusinessRule):
    """Business rule ensuring a message is not empty.

    The rule is broken when the supplied message is either ``None`` or
    contains only whitespace. This class could be renamed to
    ``MessageCannotBeEmptyRule`` but is retained as-is for backward
    compatibility. Imports updated to the correct package.
    """

    message: str
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Message cannot be empty.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        # Broken when message is empty or whitespace-only
        return not bool(self.message and self.message.strip())
