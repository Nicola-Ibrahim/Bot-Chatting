from typing import Any

from ...model.repository import IUserRepository
from ..interfaces.notification_service import INotificationService
from ..interfaces.password_hashing import IPasswordHasher
from ..use_case.exceptions import (
    RepositoryError,
    ServiceError,
    UserNotCreatedException,
    UserNotDeletedError,
    UserNotFoundError,
    UserNotUpdatedError,
    UserObjNotFoundError,
    UserSaveError,
)
from .utils import send_account_verification_otp_email
from .validation import AbstractUserValidator


class UserService:
    def __init__(
        self,
        user_repository: IUserRepository,
        user_data_validator: AbstractUserValidator,
        otp_service: INotificationService,
    ):
        self.user_repository = user_repository
        self.user_data_validator = user_data_validator
        self.otp_service = otp_service

    def create_user(self, request, data: dict[str, Any]) -> User:
        """Creates a new user after validating the data."""
        self.user_data_validator.validate_create_user_data(data)

        try:
            user = self.user_repository.create_user(data)
        except UserSaveError:
            raise UserNotCreatedException()
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
