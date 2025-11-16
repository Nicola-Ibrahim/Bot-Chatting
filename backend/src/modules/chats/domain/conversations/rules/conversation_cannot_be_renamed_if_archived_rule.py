from dataclasses import dataclass

"""Business rule disallowing renaming of archived conversations.

When ``is_archived`` is ``True``, renaming operations must fail. The
``is_broken`` method therefore returns ``True`` when the conversation is
archived. Imports corrected to reference ``src.building_blocks``.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeRenamedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONFLICT_ERROR
    message = "Conversation cannot be renamed if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # Renaming is invalid once a conversation has been archived
        return bool(self.is_archived)
