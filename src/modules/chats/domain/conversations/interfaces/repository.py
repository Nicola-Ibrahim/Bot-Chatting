from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def find(self, id: str) -> Any:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def find_all(self, id: list[str]) -> list[Any]:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def save(self, obj: Any) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def update(self, obj: Any) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def exists(self, id: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def count(self, id: str) -> int:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def delete_all(self, id: list[str]) -> None:
        raise NotImplementedError("Subclasses must implement this method.")
