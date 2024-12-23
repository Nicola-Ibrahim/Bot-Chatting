from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


class ContentIndexMustBeValidRule(BaseBusinessRule):
    def __init__(self, content_index, contents_length):
        self.content_index = content_index
        self.contents_length = contents_length
        self.code = ErrorCode.INVALID_INPUT
        self.message = "Content index must be valid."
        self.error_type = ErrorType.VALIDATION_ERROR

    def is_satisfied(self) -> bool:
        return 0 <= self.content_index < self.contents_length
