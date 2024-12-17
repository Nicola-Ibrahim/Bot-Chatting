from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def encode(self, password: str) -> str:
        """Encode the password for secure storage."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that a plain password matches the hashed password."""
        pass
