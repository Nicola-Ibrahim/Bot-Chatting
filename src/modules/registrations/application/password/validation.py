from django.contrib.auth.password_validation import get_default_password_validators

from ...models import User
from .exceptions import IncorrectPasswordError


def check_password(user: User, raw_password: str) -> bool:
    is_correct = user.check_password(raw_password)
    if not is_correct:
        raise IncorrectPasswordError()
    return True


def validate_password(password, user=None, password_validators=None) -> bool:
    """
    Validate that the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        validator.validate(password, user)

    return True
