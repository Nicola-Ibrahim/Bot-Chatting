from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .enums import ErrorCode, ErrorType


@dataclass
class BaseBusinessRule(ABC):
    """Base type for business rules enforced by entities and value objects."""

    code: ErrorCode = field(default=ErrorCode.BUSINESS_RULE_VIOLATION, init=False)
    message: str = field(default="Business rule violated.", init=False)
    error_type: ErrorType = field(default=ErrorType.BUSINESS_RULE_VIOLATION, init=False)

    @abstractmethod
    def is_broken(self) -> bool:
        """Check if the business rule is satisfied."""
