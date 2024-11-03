from ...interfaces.notification_service import INotificationService
from ...interfaces.password_hashing import IPasswordHasher
from ...interfaces.user_repository import IUserRepository


class UserRegistrationService:
    def __init__(
        self,
        user_factory,
        user_repository: IUserRepository,
        notification_service: INotificationService,
        password_hasher: IPasswordHasher,
    ):
        self.user_factory = user_factory
        self.user_repository = user_repository
        self.notification_service = notification_service
        self.password_hasher = password_hasher

    def register_user(self, email: str, username: str, password: str):
        # Step 1: Validate input (optional: can be handled in domain layer if rules are complex)
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if self.user_repository.exists_by_email(email):
            raise ValueError("Email already in use")

        # Step 2: Create User entity
        user = self.user_factory.create_user(
            email=email,
            password=self.password_hasher.encode(password),
            username=username,
            roles=["user"],  # assigning default role
        )

        # Step 3: Persist user
        self.user_repository.save(user)

        # Step 4: Trigger a welcome notification
        self.notification_service.send_welcome_email(user.email)

        # Return a success message or user data as confirmation
        return {"status": "success", "user_id": user.uuid}

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Simple email validation logic here
        return "@" in email and "." in email
