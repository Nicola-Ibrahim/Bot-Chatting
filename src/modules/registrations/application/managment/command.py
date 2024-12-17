from typing import Callable

from ...domain.model.root_entity import User
from ..interfaces.notification_service import INotificationService
from ..interfaces.repository import IUserRepository
from ...domain.model.exceptions import UserNotCreatedException


class UserCommandUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        notification_service: INotificationService,
        db_session: Callable[[], ContextManager[Session]],
    ) -> None:
        self.user_repo = user_repo
        self.db_session = db_session
        self.notification_service = notification_service

    def create_user(self, name, username, email, raw_password, permissions, phone):
        user = User.make(user)

        with self.db_session() as session:
            user: User | None = self.user_repo.save(session=session, user=user)

        if user is None:
            raise UserNotCreatedException()

        self.notification_service.send(user=user)

        return user

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

    def login(self, email: str):
        user = IUserRepository.find_by_email(email=email)

        user.login()

        # Access the JWT token generator and return it
