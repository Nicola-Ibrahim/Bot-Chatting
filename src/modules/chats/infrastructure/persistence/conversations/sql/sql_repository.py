from .....domain.conversations.interfaces.repository import AbstractConversationRepository
from .....domain.conversations.root import Conversation
from .model import Conversation


class SQLConversationRepository(AbstractConversationRepository):
    def delete(self, conversation_id: str) -> None:
        """Delete a conversation by its ID."""
        conversation = self.find(conversation_id)
        if conversation:
            conversation.manager.delete(conversation)

    def find(self, conversation_id: str) -> Conversation:
        """Find a conversation by its ID."""
        return Conversation.manager.find(conversation_id)

    def find_all(self, user_id: str) -> list[Conversation]:
        """Find all conversations for a user."""
        return Conversation.manager.find_all(user_id)

    def save(self, conversation: Conversation) -> None:
        """Save a conversation."""
        conversation.manager.save(conversation)

    def update(self, conversation: Conversation) -> None:
        """Update a conversation."""
        conversation.manager.update(conversation)

    def exists(self, conversation_id: str) -> bool:
        """Check if a conversation exists by its ID."""
        return Conversation.manager.exists(conversation_id)

    def count(self, user_id: str) -> int:
        """Count the number of conversations for a user."""
        return Conversation.manager.count(user_id)

    def delete_all(self, user_id: str) -> None:
        """Delete all conversations for a user."""
        Conversation.manager.delete_all(user_id)
