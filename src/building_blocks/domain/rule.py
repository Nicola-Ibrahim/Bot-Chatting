from dataclasses import dataclass

from .enums import ErrorCode, ErrorType


@dataclass
class BaseBusinessRule:
    code: ErrorCode
    message: str
    error_type: ErrorType

    def is_valid(self) -> bool:
        return True
