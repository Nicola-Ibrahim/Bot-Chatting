"""Rule ensuring hashed passwords are non-empty."""

from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(slots=True)
class HashedPasswordMustBeSetRule(BaseBusinessRule):
    """Ensure the hashed password string is present."""

    hashed_password: str
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Hashed password cannot be empty."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return not self.hashed_password.strip()
