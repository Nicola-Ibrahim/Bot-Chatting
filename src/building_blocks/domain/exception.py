from dataclasses import dataclass

from .enums import ErrorCode, ErrorType
from .rule import BaseBusinessRule


@dataclass
class BusinessRuleValidationException(Exception):
    """Base class for domain-specific exceptions."""

    code: ErrorCode
    message: str
    error_type: ErrorType

    def __post_init__(self, rule: BaseBusinessRule):
        self.code = rule.code
        self.error_type = rule.error_type
        self.message = rule.message
