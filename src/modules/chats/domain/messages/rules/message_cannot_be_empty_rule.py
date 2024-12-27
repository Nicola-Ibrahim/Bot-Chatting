from dataclasses import dataclass
from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class NonEmptyMessageRule(BaseBusinessRule):
    message: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Message cannot be empty."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_satisfied(self) -> bool:
        return bool(self.message and self.message.strip())
