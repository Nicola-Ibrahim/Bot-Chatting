from dataclasses import dataclass

"""Business rule preventing removal of a participant who is not part of the conversation.

If a participant with the given ID does not exist in the conversation, the rule
is broken. Imports corrected to reference ``src``.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule

from ..value_objects.participant import Participant


@dataclass
class ParticipantCannotBeRemovedIfNotExistsRule(BaseBusinessRule):
    participants: list[Participant]
    participant_id: str

    code = ErrorCode.CONFLICT_ERROR
    message = "Participant cannot be removed if they do not exist in the conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # The rule is broken when no participant with this ID exists in the collection
        return not any(p.id == self.participant_id for p in self.participants)
