from abc import ABC, abstractmethod
from typing import Iterable, Optional

from ..root import Message


class AbstractMessageRepository(ABC):
    """Persistence contract for message aggregates."""

    @abstractmethod
    def get_by_id(self, message_id: str) -> Optional[Message]:
        raise NotImplementedError

    @abstractmethod
    def list_for_conversation(self, conversation_id: str) -> Iterable[Message]:
        raise NotImplementedError

    @abstractmethod
    def save(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, message_id: str) -> None:
        raise NotImplementedError
