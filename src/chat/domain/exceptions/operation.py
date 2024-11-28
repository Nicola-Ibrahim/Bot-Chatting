from src.shared.domain.exception import BaseDomainException


class InValidOperationException(BaseDomainException):
    """Base exception for all business rule validation errors."""

    pass
