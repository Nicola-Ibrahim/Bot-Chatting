"""Rule ensuring sessions expire in the future."""

from dataclasses import dataclass
from datetime import datetime, timezone

from src.building_blocks.domain.enums import ErrorCode, ErrorType
from src.building_blocks.domain.rule import BaseBusinessRule


@dataclass(slots=True)
class SessionExpirationMustBeFutureRule(BaseBusinessRule):
    expires_at: datetime
    code: ErrorCode = ErrorCode.INVALID_INPUT
    message: str = "Session expiration must be in the future."
    error_type: ErrorType = ErrorType.VALIDATION_ERROR

    def is_broken(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)
