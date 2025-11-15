"""Business rule ensuring that a conversation creator has a non-empty name.

This rule is considered broken when the provided name is either ``None`` or
consists solely of whitespace. While some earlier implementations
attempted to reference a non-existent ``CREATOR_REMOVAL_ERROR`` code,
the correct approach is to use the generic ``INVALID_INPUT`` error code
along with a validation error type. When the rule is broken, a
``BusinessRuleValidationException`` should be raised by the caller.
"""

from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class CreatorNameCannotBeEmptyRule(BaseBusinessRule):
    name: str

    # Use a generic invalid input code since no specific code exists for
    # creator name validation
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "The name of the creator cannot be empty."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        """
        Determine whether the rule is broken.

        Returns ``True`` when ``name`` is ``None`` or consists only of
        whitespace. This signals to the calling context that a
        ``BusinessRuleValidationException`` should be raised.
        """
        return not bool(self.name and self.name.strip())
