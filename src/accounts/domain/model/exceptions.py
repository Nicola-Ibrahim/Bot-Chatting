from enum import Enum

from apps.core.shared.base_exceptions import BaseDomainException
from django.utils.translation import gettext as _


class ExceptionCode(Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_OBJECT_NOT_FOUND = "USER_OBJECT_NOT_FOUND"
    USER_NOT_CREATED = "USER_NOT_CREATED"
    USER_INACTIVE = "USER_INACTIVE"
    USER_NOT_VERIFIED = "USER_NOT_VERIFIED"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    MISSING_FIELD = "MISSING_FIELD"
    ACCOUNT_NOT_VERIFIED = "ACCOUNT_NOT_VERIFIED"
    ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"
    USER_SAVE_Exception = "USER_SAVE_Exception"
    USER_DELETE_Exception = "USER_DELETE_Exception"
    REPOSITORY_Exception = "REPOSITORY_Exception"
    SERVICE_Exception = "SERVICE_Exception"
    USER_NOT_UPDATED = "USER_NOT_UPDATED"
    USER_NOT_DELETED = "USER_NOT_DELETED"


class RepositoryException(BaseDomainException):
    """Base class for repository Exceptions."""

    def __init__(
        self,
        message="An Exception occurred while accessing the repository.",
        code=ExceptionCode.REPOSITORY_Exception,
        details=None,
    ):
        if details is None:
            details = "There was a general Exception in the repository. This could be due to a database connection issue or another unexpected failure."

        if isinstance(code, Enum):
            code = code.value

        super().__init__(message=message, code=code, details=details)


class BusinessRuleException(BaseDomainException):
    """Base class for service-related Exceptions."""

    def __init__(
        self,
        message="An Exception occurred in the service layer.",
        code=ExceptionCode.SERVICE_Exception,
        details=None,
    ):
        if details is None:
            details = "There was a general Exception in the service layer. Please try again later."

        if isinstance(code, Enum):
            code = code.value

        super().__init__(message=message, code=code, details=details)


class UserNotUpdatedException(BusinessRuleException):
    """Exception raised when a user cannot be updated."""

    def __init__(
        self,
        message=_("Failed to update user information."),
        code=ExceptionCode.USER_NOT_UPDATED,
        details="There was an Exception while trying to update the user information. Please try again later.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserNotDeletedException(BusinessRuleException):
    """Exception raised when a user cannot be deleted."""

    def __init__(
        self,
        message=_("Failed to delete user."),
        code=ExceptionCode.USER_NOT_DELETED,
        details="There was an Exception while trying to delete the user. Please try again later.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserNotFoundException(BusinessRuleException):
    """Exception raised when the user is not found."""

    def __init__(
        self,
        message=_("We couldn't find your account. Please check the email address or sign up."),
        code=ExceptionCode.USER_NOT_FOUND,
        details="The email address you provided does not match any account in our system. Please check and try again or create a new account.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserAlreadyExistsException(BusinessRuleException):
    """Exception raised when a user with the provided email already exists."""

    def __init__(
        self,
        message=_("This email is already associated with an account."),
        code=ExceptionCode.USER_ALREADY_EXISTS,
        details="Please use a different email address, or if you already have an account, try logging in or resetting your password.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserNotCreatedException(BusinessRuleException):
    """Exception raised when a user cannot be created."""

    def __init__(
        self,
        message=_("We encountered an issue while creating your account. Please check your details and try again."),
        code=ExceptionCode.USER_NOT_CREATED,
        details="There was a problem creating your account. Ensure all required fields are filled out correctly and try again. If the problem persists, please contact support.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class InvalidEmailException(BusinessRuleException):
    """Exception raised when the provided email is invalid."""

    def __init__(
        self,
        message=_("The provided email is invalid."),
        code=ExceptionCode.INVALID_EMAIL,
        details="Ensure that the email address follows the correct format (e.g., example@example.com).",
    ):
        super().__init__(message=message, code=code.value, details=details)


class InvalidPasswordException(BusinessRuleException):
    """Exception raised when the provided password does not meet the required strength."""

    def __init__(
        self,
        message=_("The provided password is too weak."),
        code=ExceptionCode.INVALID_PASSWORD,
        details="Password must be at least 8 characters long and include a mix of letters, numbers, and symbols.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class MissingFieldException(BusinessRuleException):
    """Exception raised when a required field is missing in the provided data."""

    def __init__(
        self,
        field,
        message=_("A required field is missing."),
        code=ExceptionCode.MISSING_FIELD,
        details="Please make sure all required fields are provided.",
    ):
        super().__init__(message=f"{message}: {field}", code=code.value, details=details)


class AccountNotVerifiedException(BusinessRuleException):
    """Exception raised when the user's account is not verified."""

    def __init__(
        self,
        message=_("The user account is not verified."),
        code=ExceptionCode.ACCOUNT_NOT_VERIFIED,
        details="Please verify your email before proceeding with login.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class AccountInactiveException(BusinessRuleException):
    """Exception raised when the user's account is inactive."""

    def __init__(
        self,
        message=_("The user account is inactive."),
        code=ExceptionCode.ACCOUNT_INACTIVE,
        details="Please contact support to reactivate your account.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserSaveException(RepositoryException):
    """Raised when a user cannot be saved to the database."""

    def __init__(
        self,
        message="We couldn't save your account at the moment. Please try again later.",
        code=ExceptionCode.USER_SAVE_Exception,
        details="There was an Exception while trying to save the user data to the database. Please try again later or contact support if the issue persists.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserDeleteException(RepositoryException):
    """Raised when a user cannot be deleted from the database."""

    def __init__(
        self,
        message="We couldn't delete your account at the moment. Please try again later.",
        code=ExceptionCode.USER_DELETE_Exception,
        details="An Exception occurred while trying to delete the user data from the database. Please contact support for further assistance.",
    ):
        super().__init__(message=message, code=code.value, details=details)


class UserObjNotFoundException(RepositoryException):
    """Raised when a user object is not found in the database."""

    def __init__(
        self,
        message="User object not found.",
        code=ExceptionCode.USER_OBJECT_NOT_FOUND,
        details="The specified user object could not be found in the database. Please verify the user ID and try again.",
    ):
        super().__init__(message=message, code=code.value, details=details)
