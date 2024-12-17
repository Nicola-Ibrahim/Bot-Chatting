from abc import ABC, abstractmethod
from typing import Optional

from .conversation import Conversation


class AbstractConversationRepository(ABC):
    """Abstract repository interface for managing conversation sessions."""

    @abstractmethod
    def get_by_id(self, chat_id: str) -> Optional[Conversation]:
        """Fetches a conversation aggregate by its ID."""

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        """Persists a conversation aggregate."""

    @abstractmethod
    def delete(self, chat_id: str) -> None:
        """Deletes a conversation aggregate by its ID."""

    @abstractmethod
    def list_all_chats(self) -> list[str]:
        """lists all conversation IDs available in the repository."""

    @abstractmethod
    def get_recent_chats(self, limit: int = 20) -> list[Conversation]:
        """Fetches a list of recent chats."""
