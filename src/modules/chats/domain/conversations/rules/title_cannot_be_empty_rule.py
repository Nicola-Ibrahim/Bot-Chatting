from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule


@dataclass
class TitleCannotBeEmptyRule(BaseBusinessRule):
    title: str

    code = ErrorCode.TITLE_VALIDATION_ERROR
    message = "The title of the conversation cannot be empty."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        return bool(self.title.strip())
