from dataclasses import dataclass

from src.building_blocks.domain.enums import BaseBusinessRule, ErrorCode, ErrorType


@dataclass
class CreatorCannotBeRemovedRule(BaseBusinessRule):
    creator_id: str
    participant_id: str

    code = ErrorCode.CREATOR_REMOVAL_ERROR
    message = "The creator of the conversation cannot be removed."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_satisfied(self) -> bool:
        return self.creator_id != self.participant_id
