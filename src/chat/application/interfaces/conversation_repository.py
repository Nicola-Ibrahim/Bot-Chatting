from abc import ABC, abstractmethod

from chat.domain.entities.conversation import Chat


class AbstractConversationRepository(ABC):
    """Abstract repository interface for managing memory storage in chat sessions."""

    @abstractmethod
    def get_by_id(self, chat_id: str) -> Chat:
        """Fetches all memory entries for the specified chat session."""
        pass

    @abstractmethod
    def save(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    def delete(self, chat_id: str) -> None:
        """Clears all stored memory entries for the specified chat session."""
        pass

    # @abstractmethod
    # def list_all_chats(self) -> list[Chat]:
    #     """Lists all chat IDs with existing memory files."""
    #     pass
