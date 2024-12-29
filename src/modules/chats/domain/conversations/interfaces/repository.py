from abc import ABC, abstractmethod

from ..root import Conversation


class AbstractConversationRepository(ABC):
    @abstractmethod
    def delete(self, conversation_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, conversation_id: str) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, user_id: str) -> list[Conversation]:
        raise NotImplementedError

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, conversation: Conversation) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, conversation_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def count(self, user_id: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, user_id: str) -> None:
        raise NotImplementedError
