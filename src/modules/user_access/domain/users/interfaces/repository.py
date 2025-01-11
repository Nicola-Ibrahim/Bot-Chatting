import uuid
from abc import ABC, abstractmethod

from ..root import User


class AbstractUserRepository(ABC):
    pass

    @abstractmethod
    def delete(self, user_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, user_id: uuid.UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, user_id: str) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, user_id: uuid.UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self, user_id: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, user_id: str) -> None:
        raise NotImplementedError
