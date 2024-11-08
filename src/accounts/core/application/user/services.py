from abc import ABC, abstractmethod
from typing import Any

from django.http import HttpRequest

from apps.core.otp.services import AbstractTOTPService

from ...models import User
from .exceptions import (
    RepositoryError,
    ServiceError,
    UserNotCreatedError,
    UserNotDeletedError,
    UserNotFoundError,
    UserNotUpdatedError,
    UserObjNotFoundError,
    UserSaveError,
)
from ....db.repositories.user import AbstractUserRepository
from .utils import send_account_verification_otp_email
from .validation import AbstractUserValidator


class AbstractUserService(ABC):
    @abstractmethod
    def verify_account(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def create_user(self, request: HttpRequest, data: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def update_user(self, user: Any, updates: dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def remove_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def retrieve_user_by_id(self, user_id: int) -> Any:
        pass

    @abstractmethod
    def retrieve_user_by_email(self, email: str) -> Any:
        pass

    @abstractmethod
    def initiate_account_verification(
        self, request: HttpRequest, user_id: int | str, user_email: str, user_full_name: str
    ) -> None:
        pass


class UserService:
    def __init__(
        self,
        user_repository: AbstractUserRepository,
        user_data_validator: AbstractUserValidator,
        otp_service: AbstractTOTPService,
    ):
        self.user_repository = user_repository
        self.user_data_validator = user_data_validator
        self.otp_service = otp_service

    def verify_account(self, user_id: int) -> bool:
        """Verifies the user's account by updating their verification status."""
        user = self.retrieve_user_by_id(user_id)

        if not user.is_verified:
            user.is_verified = True
            try:
                self.user_repository.update_user(user, {"is_verified": True})
            except Exception:
                raise UserNotUpdatedError("Failed to update user verification status.")

        return True

    def create_user(self, request: HttpRequest, data: dict[str, Any]) -> User:
        """Creates a new user after validating the data."""
        self.user_data_validator.validate_create_user_data(data)

        try:
            user = self.user_repository.create_user(data)
        except UserSaveError:
            raise UserNotCreatedError()
        except RepositoryError:
            raise ServiceError()

        else:
            otp_token = self.otp_service.generate_totp_token(request=request, user_id=user.pk)

            send_account_verification_otp_email(
                request=request,
                otp_token=otp_token,
                recipient_id=user.id,
                recipient_full_name=user.get_full_name(),
                recipient_email=user.email,
            )

        return user

    def update_user(self, user: User, updates: dict[str, Any]) -> User:
        """Updates the specified user's fields."""
        self.user_data_validator.validate_update_user_data(updates)

        try:
            updated_user = self.user_repository.update_user(user, updates)
        except UserSaveError:
            raise UserNotUpdatedError()
        except RepositoryError:
            raise ServiceError()

        return updated_user

    def remove_user(self, user_id: int) -> bool:
        """Removes the user associated with the given user ID."""
        try:
            self.user_repository.remove_user(user_id=user_id)
        except RepositoryError:
            raise UserNotDeletedError()

        return True

    def retrieve_user_by_id(self, user_id: int) -> User:
        """Retrieves the user associated with the given ID."""
        try:
            return self.user_repository.get_user_by_id(user_id=user_id)
        except UserObjNotFoundError:
            raise UserNotFoundError()

    def retrieve_user_by_email(self, email: str) -> User:
        """Retrieves the user associated with the given email."""
        try:
            return self.user_repository.get_user_by_email(email=email)
        except UserObjNotFoundError:
            raise UserNotFoundError()

    def initiate_account_verification(
        self, request: HttpRequest, user_id: int | str, user_email: str, user_full_name: str
    ) -> None:
        """
        Generates an OTP token and sends an email to the user with the login URL.
        """
        otp_token = self.otp_service.generate_totp_token(request=request, user_id=user_id)

        send_account_verification_otp_email(
            request=request,
            otp_token=otp_token,
            recipient_id=user_id,
            recipient_full_name=user_full_name,
            recipient_email=user_email,
        )
