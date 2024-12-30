from ....application.interfaces.conversation_repository import (
    AbstractConversationRepository,
)
from ....domain.conversations.root import Conversation
from .file_handler import JsonFileHandler
from .mapper import JsonConversationMapper


class JsonFileConversationRepository(AbstractConversationRepository):
    """
    Repository for managing conversation data stored in JSON files.
    """

    def __init__(self):
        self.file_handler = JsonFileHandler(directory="conversation_data")

    def get_by_id(self, conversation_id: str) -> Conversation:
        """
        Fetches a conversation aggregate by ID.

        Args:
            conversation_id (str): Unique identifier for the conversation.

        Returns:
            Conversation: The Conversation domain model.
        """
        data = self.file_handler.read(conversation_id)
        return JsonConversationMapper.conversation_from_json(data)

    def save(self, conversation: Conversation) -> None:
        """
        Saves or updates a conversation aggregate.

        Args:
            conversation (Conversation): The Conversation domain model to save.
        """
        data = JsonConversationMapper.conversation_to_json(conversation)
        self.file_handler.write(conversation.id, data)

    def delete(self, conversation_id: str) -> None:
        """
        Deletes a conversation by ID.

        Args:
            conversation_id (str): Unique identifier for the conversation.
        """
        self.file_handler.delete(conversation_id)

    def list_all_conversations(self) -> list[str]:
        """
        Lists all existing conversation IDs.

        Returns:
            list[str]: List of conversation IDs.
        """
        return self.file_handler.list_files()
