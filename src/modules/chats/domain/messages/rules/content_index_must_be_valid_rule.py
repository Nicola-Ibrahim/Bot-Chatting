from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentIndexMustBeValidRule(BaseBusinessRule):
    content_index: int
    contents_length: int
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Content index must be valid."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return 0 <= self.content_index < self.contents_length
