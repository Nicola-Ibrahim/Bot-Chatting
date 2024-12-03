from .base import BaseDomainException


class InValidOperationException(BaseDomainException):
    """Base exception for all business rule validation errors."""
