from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeDeletedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONVERSATION_DELETION_ERROR
    message = "Conversation cannot be deleted if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_satisfied(self) -> bool:
        return not self.is_archived
