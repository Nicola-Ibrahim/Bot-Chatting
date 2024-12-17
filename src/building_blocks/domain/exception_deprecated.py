from dataclasses import dataclass


@dataclass
class BusinessRuleValidationException(Exception):
    """Base class for domain-specific exceptions."""

    code: ErrorCode
    description: str
    error_type: ErrorType

    def __post_init__(self):
        # Initialize the message using the code and description
        self.message = f"{self.error_type.value}: {self.code.value} - {self.description}"
        super().__init__(self.message)

    @classmethod
    def failure(cls, description: str) -> "BusinessRuleValidationException":
        """Create a failure exception."""
        return cls(ErrorCode.FAILURE, description, ErrorType.FAILURE)

    @classmethod
    def not_found(cls, description: str) -> "BusinessRuleValidationException":
        """Create a not found exception."""
        return cls(ErrorCode.NOT_FOUND, description, ErrorType.NOT_FOUND)

    @classmethod
    def validation(cls, description: str) -> "BusinessRuleValidationException":
        """Create a validation exception."""
        return cls(ErrorCode.INVALID_INPUT, description, ErrorType.VALIDATION)

    @classmethod
    def conflict(cls, description: str) -> "BusinessRuleValidationException":
        """Create a conflict exception."""
        return cls(ErrorCode.CONFLICT, description, ErrorType.CONFLICT)

    @classmethod
    def access_unauthorized(cls, description: str) -> "BusinessRuleValidationException":
        """Create an unauthorized access exception."""
        return cls(ErrorCode.UNAUTHORIZED, description, ErrorType.UNAUTHORIZED)

    @classmethod
    def access_forbidden(cls, description: str) -> "BusinessRuleValidationException":
        """Create a forbidden access exception."""
        return cls(ErrorCode.FORBIDDEN, description, ErrorType.FORBIDDEN)

    def to_dict(self) -> dict:
        """
        Convert the exception details to a dictionary.

        Returns:
            dict: A dictionary containing the exception details.
        """
        return {
            "code": self.code.value,
            "description": self.description,
            "error_type": self.error_type.value,
        }
