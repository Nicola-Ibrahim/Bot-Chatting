from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


class InitialContentMustBeProvidedRule(BaseBusinessRule):
    def __init__(self, content):
        self.content = content
        self.code = ErrorCode.INVALID_INPUT
        self.message = "Initial content must be provided."
        self.error_type = ErrorType.VALIDATION_ERROR

    def is_satisfied(self) -> bool:
        return bool(self.content)
