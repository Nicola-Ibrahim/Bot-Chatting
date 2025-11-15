from dataclasses import dataclass

"""Business rule ensuring a message is not empty.

The rule is broken when the supplied message is either ``None`` or
contains only whitespace. This class could be renamed to
``MessageCannotBeEmptyRule`` but is retained as-is for backward
compatibility. Imports updated to the correct package.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class NonEmptyMessageRule(BaseBusinessRule):
    message: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Message cannot be empty."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        # Broken when message is empty or whitespace-only
        return not bool(self.message and self.message.strip())
