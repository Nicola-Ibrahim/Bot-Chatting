import re
from difflib import SequenceMatcher

from django.contrib.auth.password_validation import CommonPasswordValidator as DjangoCommonPasswordValidator
from django.contrib.auth.password_validation import MinimumLengthValidator as DjangoMinimumLengthValidator
from django.contrib.auth.password_validation import NumericPasswordValidator as DjangoNumericPasswordValidator
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator as DjangoUserAttributeSimilarityValidator,
)
from django.contrib.auth.password_validation import exceeds_maximum_length_ratio
from django.core.exceptions import FieldDoesNotExist
from django.utils.translation import gettext as _

from .exceptions import (
    PasswordEntirelyNumericError,
    PasswordTooCommonError,
    PasswordTooShortError,
    PasswordTooSimilarError,
)


class MinimumLengthValidator(DjangoMinimumLengthValidator):
    """
    Validate that the password is of a minimum length.
    """

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise PasswordTooShortError(min_length=self.min_length)


class UserAttributeSimilarityValidator(DjangoUserAttributeSimilarityValidator):
    """
    Validate that the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """

    def validate(self, password, user=None):
        if not user:
            return

        password = password.lower()
        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_lower = value.lower()
            value_parts = re.split(r"\W+", value_lower) + [value_lower]
            for value_part in value_parts:
                if exceeds_maximum_length_ratio(password, self.max_similarity, value_part):
                    continue
                if SequenceMatcher(a=password, b=value_part).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise PasswordTooSimilarError(attribute_name=verbose_name)


class CommonPasswordValidator(DjangoCommonPasswordValidator):
    """
    Validate that the password is not a common password.

    The password is rejected if it occurs in a provided list of passwords,
    which may be gzipped. The list Django ships with contains 20000 common
    passwords (lowercased and deduplicated), created by Royce Williams:
    https://gist.github.com/roycewilliams/226886fd01572964e1431ac8afc999ce
    The password list must be lowercased to match the comparison in validate().
    """

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise PasswordTooCommonError()


class NumericPasswordValidator(DjangoNumericPasswordValidator):
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise PasswordEntirelyNumericError()
