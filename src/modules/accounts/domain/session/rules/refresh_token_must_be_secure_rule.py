"""Rule ensuring refresh tokens are sufficiently random."""

from dataclasses import dataclass

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(slots=True)
class RefreshTokenMustBeSecureRule(BaseBusinessRule):
    token: str
    min_length: int = 32
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Refresh token is too short."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return not self.token or len(self.token) < self.min_length
