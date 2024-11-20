from ....application.interface.chat_repository import AbstractChatRepository
from ....domain.value_objects.chat import Chat
from .file_handler import JsonFileHandler
from .mapper import JsonChatMapper


class JsonFileMemoryRepository(AbstractChatRepository):
    """
    Repository for managing chat data stored in JSON files.
    """

    def __init__(self):
        self.file_handler = JsonFileHandler("chat_memories")

    def get_by_id(self, chat_id: str) -> Chat:
        """
        Fetches a chat aggregate by ID.

        Args:
            chat_id (str): Unique identifier for the chat.

        Returns:
            Chat: The Chat domain model.
        """
        data = self.file_handler.read(chat_id)
        return JsonChatMapper.chat_from_json(data)

    def save(self, chat: Chat) -> None:
        """
        Saves or updates a chat aggregate.

        Args:
            chat (Chat): The Chat domain model to save.
        """
        data = JsonChatMapper.chat_to_json(chat)
        self.file_handler.write(chat.id, data)

    def delete(self, chat_id: str) -> None:
        """
        Deletes a chat by ID.

        Args:
            chat_id (str): Unique identifier for the chat.
        """
        self.file_handler.delete(chat_id)

    # def list_all_chats(self) -> list[str]:
    #     """
    #     Lists all existing chat IDs.

    #     Returns:
    #         list[str]: List of chat IDs.
    #     """
    #     return self.file_handler.list_files()
