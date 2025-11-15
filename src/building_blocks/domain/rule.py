from abc import ABC, abstractmethod
from dataclasses import dataclass

from .enums import ErrorCode, ErrorType


@dataclass
class BaseBusinessRule(ABC):
    """Base type for business rules enforced by entities and value objects."""

    code: ErrorCode = ErrorCode.BUSINESS_RULE_VIOLATION
    message: str = "Business rule violated."
    error_type: ErrorType = ErrorType.BUSINESS_RULE_VIOLATION

    @abstractmethod
    def is_broken(self) -> bool:
        """Check if the business rule is satisfied."""
