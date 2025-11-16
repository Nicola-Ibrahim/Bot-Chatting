from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentResponseMustBeValidRule(BaseBusinessRule):
    response: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Response must be valid."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return not self.response or len(self.response) < 5
