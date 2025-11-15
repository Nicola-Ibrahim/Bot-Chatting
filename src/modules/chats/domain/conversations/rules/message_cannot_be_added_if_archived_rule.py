from dataclasses import dataclass

"""Business rule blocking message addition to archived conversations.

If the conversation has been archived, new messages cannot be added. This
rule is broken when ``is_archived`` is ``True``. Imports updated to use
the correct ``src`` prefix.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class MessageCannotBeAddedIfArchivedRule(BaseBusinessRule):
    is_archived: bool

    code = ErrorCode.CONFLICT_ERROR
    message = "Messages cannot be added to an archived conversation."
    error_type = ErrorType.BUSINESS_RULE_VIOLATION

    def is_broken(self) -> bool:
        return bool(self.is_archived)
