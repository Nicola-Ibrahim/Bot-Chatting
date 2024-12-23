from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


class MessageMustExistRule(BaseBusinessRule):
    def __init__(self, message):
        self.message = message
        self.code = ErrorCode.ENTITY_NOT_FOUND
        self.message = "Message must exist."
        self.error_type = ErrorType.ENTITY_NOT_FOUND

    def is_satisfied(self) -> bool:
        return self.message is not None
