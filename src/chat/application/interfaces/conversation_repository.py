from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.conversation import Conversation


class AbstractConversationRepository(ABC):
    """Abstract repository interface for managing conversation sessions."""

    @abstractmethod
    def get_by_id(self, chat_id: str) -> Optional[Conversation]:
        """Fetches a conversation aggregate by its ID."""
        pass

    @abstractmethod
    def save(self, conversation: Conversation) -> None:
        """Persists a conversation aggregate."""
        pass

    @abstractmethod
    def delete(self, chat_id: str) -> None:
        """Deletes a conversation aggregate by its ID."""
        pass

    @abstractmethod
    def list_all_chats(self) -> List[str]:
        """Lists all conversation IDs available in the repository."""
        pass

    @abstractmethod
    def get_recent_chats(self, limit: int = 20) -> List[Conversation]:
        """Fetches a list of recent chats."""
        pass
