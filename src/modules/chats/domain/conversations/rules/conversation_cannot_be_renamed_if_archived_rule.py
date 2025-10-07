from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ConversationCannotBeRenamedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONVERSATION_RENAMING_ERROR
    message = "Conversation cannot be renamed if it is archived."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        return not self.is_archived
