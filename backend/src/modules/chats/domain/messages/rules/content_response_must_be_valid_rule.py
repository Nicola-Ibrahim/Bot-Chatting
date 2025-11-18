from dataclasses import dataclass, field

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass
class ContentResponseMustBeValidRule(BaseBusinessRule):
    response: str
    code: ErrorCode = field(default=ErrorCode.INVALID_INPUT, init=False)
    message: str = field(
        default="Content response must be valid and sufficiently detailed.",
        init=False,
    )
    error_type: ErrorType = field(default=ErrorType.VALIDATION_ERROR, init=False)

    def is_broken(self) -> bool:
        return not self.response or len(self.response) < 5
