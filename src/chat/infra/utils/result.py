from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from ...domain.exceptions.exception import BaseDomainException

T = TypeVar("T")  # Type of the success value
E = TypeVar("E", bound=BaseDomainException)  # Type of the error (must be an exception)


@dataclass
class Result(Generic[T, E]):
    """
    Class for encapsulating the outcome of an operation,
    which can either succeed (SuccessResult) or fail (ErrorResult).
    """

    _value: T | None = None
    _error: E | None = None

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

    def map(self, fn: Callable[[T], T]) -> "Result[T, E]":
        """
        Transforms the value of a successful result.

        Args:
            fn (Callable): Function to apply on the success value.

        Returns:
            Result[T, E]: A new result with the transformed value.
        """
        if self.is_ok:
            return Result.ok(fn(self.value))
        return self

    def flat_map(self, fn: Callable[[T], "Result[Any, E]"]) -> "Result[Any, E]":
        """
        Applies a function that returns a `Result` and flattens the result.

        Args:
            fn (Callable): Function that returns a `Result`.

        Returns:
            Result[Any, E]: A flattened result.
        """
        if self.is_ok:
            return fn(self.value)
        return self

    def on_failure(self, fn: Callable[[E], Any]) -> "Result[T, E]":
        """
        Executes a function when the result is a failure (i.e., has an error).

        Args:
            fn (Callable): Function to execute on failure.

        Returns:
            Result[T, E]: This result (unchanged).
        """
        if self.is_failure:
            fn(self.error)
        return self

    def unwrap(self) -> T:
        """
        Returns the success value or raises an error if the result is a failure.

        Returns:
            T: The success value.

        Raises:
            ValueError: If the result is a failure.
        """
        if self.is_failure:
            raise ValueError(f"Unwrap failed with error: {self.error}")
        return self.value

    def __repr__(self) -> str:
        """
        Custom repr for better debugging.
        """
        if self.is_ok:
            return f"Result.ok({repr(self._value)})"
        return f"Result.fail({repr(self._error)})"

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
