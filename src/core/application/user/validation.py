from abc import ABC, abstractmethod
from typing import Any

from ...models import User
from ..password_management.validation import check_password
from .exceptions import (
    AccountInactiveError,
    AccountNotVerifiedError,
    InvalidEmailError,
    InvalidPasswordError,
    MissingFieldError,
    UserAlreadyExistsError,
)
from ....db.repositories.user import AbstractUserRepository


class AbstractUserValidator(ABC):
    @abstractmethod
    def validate_create_user_data(self, data: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def validate_update_user_data(self, updates: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def validate_email_format(self, email: str) -> None:
        pass

    @abstractmethod
    def validate_password_strength(self, password: str) -> None:
        pass

    @abstractmethod
    def validate_user_password(self, user: Any, password: str) -> None:
        pass

    @abstractmethod
    def validate_user_not_exists(self, email: str) -> None:
        pass

    @abstractmethod
    def validate_user_active(self, user_id: int | str) -> None:
        pass

    @abstractmethod
    def validate_user_verified(self, user_id: int | str) -> None:
        pass


class UserValidator(AbstractUserValidator):
    def __init__(self, user_repository: AbstractUserRepository) -> None:
        self.user_repository = user_repository

    def validate_create_user_data(self, data: dict[str, Any]) -> None:
        required_fields = ["email", "password"]
        for field in required_fields:
            if field not in data:
                raise MissingFieldError(f"{field} is required.")

        self.validate_email_format(data["email"])
        self.validate_password_strength(data["password"])
        self.validate_user_not_exists(data["email"])

    def validate_update_user_data(self, updates: dict[str, Any]) -> None:
        if "email" in updates:
            self.validate_email_format(updates["email"])

        if "password" in updates:
            self.validate_password_strength(updates["password"])

    def validate_email_format(self, email: str) -> None:
        if not isinstance(email, str) or "@" not in email:
            raise InvalidEmailError()

    def validate_password_strength(self, password: str) -> None:
        if len(password) < 8:
            raise InvalidPasswordError()

    def validate_user_password(self, user: User, password: str) -> None:
        if not check_password(user=user, raw_password=password):
            raise InvalidPasswordError()

    def validate_user_not_exists(self, email: str) -> None:
        if not isinstance(email, str):
            raise ValueError("Email must be a string.")

        exists = self.user_repository.check_user_exists(email)
        if exists:
            raise UserAlreadyExistsError()

    def validate_user_active(self, user_id: int | str) -> None:
        if not self.user_repository.is_user_active(user_id=user_id):
            raise AccountInactiveError()

    def validate_user_verified(self, user_id: int | str) -> None:
        if not self.user_repository.is_user_verified(user_id=user_id):
            raise AccountNotVerifiedError()
