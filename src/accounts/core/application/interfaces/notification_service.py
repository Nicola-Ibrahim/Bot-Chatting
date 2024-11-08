from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    def send_welcome_email(self, email: str) -> None:
        """Send a welcome email to the user."""
        pass

    @abstractmethod
    def send_password_reset_email(self, email: str) -> None:
        """Send a password reset email to the user."""
        pass


class IPasswordHasher(ABC):
    @abstractmethod
    def encode(self, password: str) -> str:
        """Encode the password for secure storage."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that a plain password matches the hashed password."""
        pass
