from dataclasses import dataclass

"""Rule ensuring a content index refers to an existing element.

The rule is broken when the index is negative or beyond the length of the
contents collection. Imports remain correct since they already reference
``src.building_blocks``.
"""

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentIndexMustBeValidRule(BaseBusinessRule):
    content_index: int
    contents_length: int
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Content index must be valid."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        # A valid index must be within the bounds [0, contents_length)
        return not (0 <= self.content_index < self.contents_length)
