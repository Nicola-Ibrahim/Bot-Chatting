from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(frozen=True)
class ContentTextMustBeValidRule(BaseBusinessRule):
    text: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Content must be valid."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return bool(self.text and len(self.text) > 0)
