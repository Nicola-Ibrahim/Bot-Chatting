from dataclasses import dataclass

"""Business rule preventing removal of the conversation creator.

The rule is broken when the ID of the participant to be removed matches
the creator's ID. When broken, the consumer of the rule should raise
a ``BusinessRuleValidationException``. Imports were corrected to reference
the appropriate ``ErrorCode`` and ``ErrorType`` from ``src.building_blocks``.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class CreatorCannotBeRemovedRule(BaseBusinessRule):
    creator_id: str
    participant_id: str

    # Use generic conflict error code since a specific one isn't defined
    code = ErrorCode.CONFLICT_ERROR
    message = "The creator of the conversation cannot be removed."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        # It is a violation if the participant slated for removal *is* the creator
        return self.creator_id == self.participant_id
