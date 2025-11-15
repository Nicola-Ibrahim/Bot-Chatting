from dataclasses import dataclass

"""Business rule preventing sharing of archived conversations.

Sharing an archived conversation is prohibited. The rule is broken when
``is_archived`` is ``True``. Imports updated to point to the correct
``src.building_blocks`` package.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeSharedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONFLICT_ERROR
    message = "Conversation cannot be shared if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # If the conversation is archived, sharing is not allowed
        return bool(self.is_archived)
