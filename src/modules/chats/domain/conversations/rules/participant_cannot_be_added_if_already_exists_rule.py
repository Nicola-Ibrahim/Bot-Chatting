from dataclasses import dataclass

"""Business rule that prevents adding a participant who already exists in the conversation.

If the provided participant ID is found in the existing participants list, the
rule is considered broken. Imports corrected to reference the ``src`` prefix.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule

from ..value_objects.participant import Participant


@dataclass
class ParticipantCannotBeAddedIfAlreadyExistsRule(BaseBusinessRule):
    participants: list[Participant]
    participant_id: str

    code = ErrorCode.CONFLICT_ERROR
    message = "Participant cannot be added if they already exist in the conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # The rule is broken if a participant with this ID already exists
        return any(p.id == self.participant_id for p in self.participants)
