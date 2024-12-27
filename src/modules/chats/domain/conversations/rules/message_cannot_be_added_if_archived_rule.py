from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule


@dataclass
class MessageCannotBeAddedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.MESSAGE_ADDITION_ERROR
    message = "Messages cannot be added to an archived conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_satisfied(self) -> bool:
        return not self.is_archived
