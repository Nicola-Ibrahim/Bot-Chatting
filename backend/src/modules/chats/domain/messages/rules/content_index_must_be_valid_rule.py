from dataclasses import dataclass, field

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentIndexMustBeValidRule(BaseBusinessRule):
    """Rule ensuring a content index refers to an existing element.

    The rule is broken when the index is negative or beyond the length of the
    contents collection. Imports remain correct since they already reference
    ``src.building_blocks``.
    """

    content_index: int
    contents_length: int
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Content index must be within the valid range of contents.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        # A valid index must be within the bounds [0, contents_length)
        return not (0 <= self.content_index < self.contents_length)
