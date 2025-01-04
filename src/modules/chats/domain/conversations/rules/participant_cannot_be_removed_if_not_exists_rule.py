from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule

from ..components.participant import Participant


@dataclass
class ParticipantCannotBeRemovedIfNotExistsRule(BaseBusinessRule):
    participants: list[Participant]
    participant_id: str

    code = ErrorCode.PARTICIPANT_REMOVAL_ERROR
    message = "Participant cannot be removed if they do not exist in the conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_satisfied(self) -> bool:
        return any(p._id == self.participant_id for p in self.participants)
