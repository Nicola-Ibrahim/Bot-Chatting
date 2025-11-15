from dataclasses import dataclass

"""Business rule preventing deletion of archived conversations.

The rule is considered broken when ``is_archived`` is ``True``. Deleting
archived conversations is disallowed. Updated imports to reference
``src.building_blocks`` instead of the relative path.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeDeletedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONFLICT_ERROR
    message = "Conversation cannot be deleted if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # Deletion is invalid when the conversation is archived
        return bool(self.is_archived)
