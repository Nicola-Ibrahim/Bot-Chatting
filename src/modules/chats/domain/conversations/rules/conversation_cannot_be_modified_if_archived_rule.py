from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeModifiedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONVERSATION_MODIFICATION_ERROR
    message = "Conversation cannot be modified if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        return not self.is_archived
