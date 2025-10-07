from dataclasses import dataclass

from building_blocks.domain.enums import ErrorCode, ErrorType
from building_blocks.domain.rule import BaseBusinessRule

from ..value_objects.participant import Participant


@dataclass
class ParticipantCannotBeAddedIfAlreadyExistsRule(BaseBusinessRule):
    participants: list[Participant]
    participant_id: str

    code = ErrorCode.PARTICIPANT_ADDITION_ERROR
    message = "Participant cannot be added if they already exist in the conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        return not any(p.id == self.participant_id for p in self.participants)
