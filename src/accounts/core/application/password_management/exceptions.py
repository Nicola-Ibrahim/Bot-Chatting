from enum import Enum

from django.utils.translation import gettext as _

from apps.core.shared.base_exceptions import BaseException


class ErrorCode(Enum):
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    PASSWORD_TOO_SHORT = "PASSWORD_TOO_SHORT"
    PASSWORD_TOO_SIMILAR = "PASSWORD_TOO_SIMILAR"
    PASSWORD_TOO_COMMON = "PASSWORD_TOO_COMMON"
    PASSWORD_ENTIRELY_NUMERIC = "PASSWORD_ENTIRELY_NUMERIC"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"


class PasswordMismatchError(BaseException):
    """Exception raised when the two password fields don't match."""

    def __init__(
        self,
        message=_("The two password fields didn't match."),
        code=ErrorCode.PASSWORD_MISMATCH,
        details=_("Please make sure both password fields contain the same value."),
    ):
        super().__init__(message=message, code=code.value, details=details)


class IncorrectPasswordError(BaseException):
    """Exception raised when the provided password is incorrect."""

    def __init__(
        self,
        message=_("Oops! The password you entered is incorrect. Please try again."),
        code=ErrorCode.INCORRECT_PASSWORD,
        details=_(
            "The password you provided doesn't match our records. Please double-check and try again. If you've forgotten your password, you can reset it using the 'Forgot Password' option."
        ),
    ):
        super().__init__(message=message, code=code.value, details=details)


class PasswordTooShortError(BaseException):
    """Exception raised when the provided password is too short."""

    def __init__(
        self,
        message=_("Your password is too short."),
        code=ErrorCode.PASSWORD_TOO_SHORT,
        details=_(
            "The password must contain at least %(min_length)d characters. Please try again with a longer password."
        ),
        min_length=8,
    ):
        self.min_length = min_length
        super().__init__(message=message, code=code.value, details=details % {"min_length": self.min_length})


class PasswordTooSimilarError(BaseException):
    """Exception raised when the provided password is too similar to user attributes."""

    def __init__(
        self,
        attribute_name,
        message=_("Your password is too similar to %(attribute)s."),
        code=ErrorCode.PASSWORD_TOO_SIMILAR,
        details=_(
            "The password you provided is too similar to your %(attribute)s. Try choosing a password that's different from personal information like your name or email."
        ),
    ):
        self.attribute_name = attribute_name
        super().__init__(
            message=message % {"attribute": attribute_name},
            code=code.value,
            details=details % {"attribute": attribute_name},
        )


class PasswordTooCommonError(BaseException):
    """Exception raised when the provided password is too common."""

    def __init__(
        self,
        message=_("Your password is too common."),
        code=ErrorCode.PASSWORD_TOO_COMMON,
        details=_(
            "The password you provided is too commonly used and may not be secure. Please try a more unique password."
        ),
    ):
        super().__init__(message=message, code=code.value, details=details)


class PasswordEntirelyNumericError(BaseException):
    """Exception raised when the provided password is entirely numeric."""

    def __init__(
        self,
        message=_("Your password cannot be entirely numeric."),
        code=ErrorCode.PASSWORD_ENTIRELY_NUMERIC,
        details=_(
            "A secure password should include a mix of numbers, letters, and symbols. Please avoid using only numbers."
        ),
    ):
        super().__init__(message=message, code=code.value, details=details)
