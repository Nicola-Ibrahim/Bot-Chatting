from enum import Enum


class ErrorType(Enum):
    """Enumeration of error types."""

    FAILURE = "Failure"
    NOT_FOUND = "NotFound"
    VALIDATION = "Validation"
    CONFLICT = "Conflict"
    UNAUTHORIZED = "AccessUnauthorized"
    FORBIDDEN = "AccessForbidden"


class ErrorCode(Enum):
    """Enumeration of error codes."""

    FAILURE = "Failure"
    INVALID_INPUT = "InvalidInput"
    NOT_FOUND = "NotFound"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    CONFLICT = "Conflict"
