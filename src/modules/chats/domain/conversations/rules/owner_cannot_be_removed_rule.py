from dataclasses import dataclass

from src.building_blocks.domain.enums import BaseBusinessRule, ErrorCode, ErrorType


@dataclass
class OwnerCannotBeRemovedRule(BaseBusinessRule):
    owner_id: str
    participant_id: str

    code = ErrorCode.OWNER_REMOVAL_ERROR
    message = "The owner of the conversation cannot be removed."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_satisfied(self) -> bool:
        return self.owner_id != self.participant_id
