from enum import Enum


class ErrorType(Enum):
    """Enumeration of error types."""

    BUSINESS_RULE_VIOLATION = "BusinessRuleViolation"
    ENTITY_NOT_FOUND = "EntityNotFound"
    VALIDATION_ERROR = "ValidationError"
    CONFLICT_ERROR = "ConflictError"
    UNAUTHORIZED_ACCESS = "UnauthorizedAccess"
    FORBIDDEN_ACCESS = "ForbiddenAccess"


class ErrorCode(Enum):
    """Enumeration of error codes."""

    BUSINESS_RULE_VIOLATION = "BusinessRuleViolation"
    INVALID_INPUT = "InvalidInput"
    ENTITY_NOT_FOUND = "EntityNotFound"
    UNAUTHORIZED_ACCESS = "UnauthorizedAccess"
    FORBIDDEN_ACCESS = "ForbiddenAccess"
    CONFLICT_ERROR = "ConflictError"
