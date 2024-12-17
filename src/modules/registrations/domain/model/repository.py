from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import UUID

from .root_entity import User


class IUserCommandRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        """Persist the user entity to the database."""
        pass

    @abstractmethod
    def remove(self, user_id: int) -> None:
        pass

    @abstractmethod
    def update(self, user_id: int) -> None:
        pass


class IUserQueryRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[Any]:
        """Retrieve a user by their unique identifier."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Any]:
        """Retrieve a user by their unique identifier."""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if a user exists by their email address."""
        pass

    @abstractmethod
    def find_all(self) -> list[Any]:
        """Retrieve all users."""
        pass

    @abstractmethod
    def check_user_exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def is_user_active(self, user_id: int | str | UUID) -> bool:
        pass

    @abstractmethod
    def is_user_verified(self, user_id: int | str | UUID) -> bool:
        pass
