from dataclasses import dataclass

"""Business rule to prevent modification of archived conversations.

This rule is broken when the conversation has been archived. In a DDD context
we signal that an operation is invalid by returning ``True`` from
``is_broken``. Updated imports to reference the correct package.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeModifiedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    # Use generic codes as specific codes are not defined in ErrorCode
    code = ErrorCode.CONFLICT_ERROR
    message = "Conversation cannot be modified if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # If the conversation is archived, modifications are not allowed
        return bool(self.is_archived)
