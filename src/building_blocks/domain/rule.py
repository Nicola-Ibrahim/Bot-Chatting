from abc import ABC, abstractmethod
from dataclasses import dataclass

from .enums import ErrorCode, ErrorType


@dataclass
class BaseBusinessRule(ABC):
    code: ErrorCode
    message: str
    error_type: ErrorType

    @abstractmethod
    def is_satisfied(self) -> bool:
        """Check if the business rule is satisfied."""
