from abc import ABC, abstractmethod
from typing import Iterable, Sequence
from uuid import UUID

from ..conversations.conversation import Conversation
from ..conversations.value_objects.conversation_id import ConversationId

ConversationKey = ConversationId | UUID | str


class BaseConversationRepository(ABC):
    @abstractmethod
    def delete(self, id: ConversationKey) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def find(self, id: ConversationKey) -> Conversation | None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def find_all(self, id: ConversationKey | Sequence[ConversationKey]) -> Iterable[Conversation]:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def save(self, obj: Conversation) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def update(self, obj: Conversation) -> None:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def exists(self, id: ConversationKey) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def count(self, id: ConversationKey) -> int:
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def delete_all(self, id: ConversationKey | Sequence[ConversationKey]) -> None:
        raise NotImplementedError("Subclasses must implement this method.")
