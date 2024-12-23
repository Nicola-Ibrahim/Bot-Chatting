from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


class ContentMustBelongToConversationRule(BaseBusinessRule):
    def __init__(self, content, conversation_id):
        self.content = content
        self.conversation_id = conversation_id
        self.code = ErrorCode.INVALID_INPUT
        self.message = "Content must belong to the conversation."
        self.error_type = ErrorType.VALIDATION_ERROR

    def is_satisfied(self) -> bool:
        return self.content.conversation_id == self.conversation_id
