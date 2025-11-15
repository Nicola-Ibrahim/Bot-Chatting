"""Business rule enforcing the password strength policy."""

from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(slots=True)
class PasswordMustMeetPolicyRule(BaseBusinessRule):
    """Ensure a password satisfies basic strength requirements."""

    password: str
    min_length: int = 8
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Password does not meet minimum strength requirements."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return not self.password or len(self.password) < self.min_length
