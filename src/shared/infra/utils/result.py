from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from ...domain.exception import BaseDomainException

T = TypeVar("T")  # Type of the success value
E = TypeVar("E", bound=BaseDomainException)  # Type of the error (must be an exception)


@dataclass
class Result(Generic[T, E]):
    """
    Class for encapsulating the outcome of an operation,
    which can either succeed (SuccessResult) or fail (ErrorResult).
    """

    _value: T = None
    _error: E = None

    def __post_init__(self):
        if self._value is not None and self._error is not None:
            raise ValueError("Result cannot have both value and error.")
        if self._value is None and self._error is None:
            raise ValueError("Result must have either value or error.")

    @property
    def is_ok(self) -> bool:
        """Check if the result represents success."""
        return self._error is None

    @property
    def is_failure(self) -> bool:
        """Check if the result represents an error."""
        return self._error is not None

    @property
    def value(self) -> T:
        """Get the success value."""
        if self.is_failure:
            raise ValueError("Cannot access value on an error result.")
        return self._value

    @property
    def error(self) -> E:
        """Get the error."""
        if self.is_ok:
            raise ValueError("Cannot access error on a success result.")
        return self._error

    def match(self, on_success: Callable[[T], Any], on_failure: Callable[[E], Any]) -> Any:
        """
        Execute appropriate function based on result type.

        Args:
            on_success (Callable): Function to handle success.
            on_failure (Callable): Function to handle error.

        Returns:
            Any: The return value of the called function.
        """
        if self.is_ok:
            return on_success(self.value)
        return on_failure(self.error)

    @classmethod
    def ok(cls, value: T) -> "Result[T, E]":
        """
        Factory method for creating a success result.

        Args:
            value (T): The value representing success.

        Returns:
            Result[T, E]: A successful result.
        """
        return cls(_value=value)

    @classmethod
    def fail(cls, error: E) -> "Result[T, E]":
        """
        Factory method for creating an error result.

        Args:
            error (E): The error representing failure.

        Returns:
            Result[T, E]: An error result.
        """
        return cls(_error=error)