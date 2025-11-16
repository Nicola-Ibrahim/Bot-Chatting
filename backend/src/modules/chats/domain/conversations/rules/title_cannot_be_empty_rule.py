from dataclasses import dataclass

"""Business rule to ensure a conversation title is not empty.

This rule is considered broken when the provided title is either an empty
string or consists solely of whitespace. When broken, the rule's code,
message and error_type are used to construct a ``BusinessRuleValidationException``
by the calling context. The imports were also updated to reference the
``src.building_blocks`` package correctly.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class TitleCannotBeEmptyRule(BaseBusinessRule):
    title: str

    # Use a general INVALID_INPUT code since no specific code exists for titles
    code = ErrorCode.INVALID_INPUT
    message = "The title of the conversation cannot be empty."
    error_type = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        """
        A title is considered invalid (broken) when it is empty or contains
        only whitespace. Return ``True`` when the rule has been violated.
        """
        # ``strip`` removes surrounding whitespace; an empty string evaluates to False
        return not bool(self.title and self.title.strip())
