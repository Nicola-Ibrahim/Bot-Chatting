from ...domain.value_objects.chat import Chat
from ..dtos.chat_dto import ChatDTO
from .prompt_mapper import MessageMapper


class ChatMapper:
    """Mapper for converting between Chat domain model and ChatDTO."""

    def to_dto(self, chat: Chat) -> ChatDTO:
        """
        Converts a Chat domain model to a ChatDTO.

        Args:
            chat (Chat): The Chat domain model.

        Returns:
            ChatDTO: Data transfer object for the Chat model.
        """
        if not isinstance(chat, Chat):
            raise TypeError(f"Expected Chat instance, got {type(chat).__name__}")

        messages_dto = [MessageMapper.to_dto(message) for message in chat.messages]
        return ChatDTO(chat_id=chat.id, messages=messages_dto)

    def from_dto(self, chat_dto: ChatDTO) -> Chat:
        """
        Converts a ChatDTO to a Chat domain model.

        Args:
            chat_dto (ChatDTO): The Chat data transfer object.

        Returns:
            Chat: Domain model for the Chat.
        """
        if not isinstance(chat_dto, ChatDTO):
            raise TypeError(f"Expected ChatDTO instance, got {type(chat_dto).__name__}")

        messages = [MessageMapper.from_dto(prompt_dto) for prompt_dto in chat_dto.messages]
        return Chat(id=chat_dto.chat_id, messages=messages)
