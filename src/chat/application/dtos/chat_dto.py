from dataclasses import dataclass, field
from typing import Any, List

from .prompt_dto import MessageDTO


@dataclass
class ChatDTO:
    """Data Transfer Object for representing a chat session with messages."""

    chat_id: str
    messages: List[MessageDTO] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the ChatDTO instance into a dictionary format for JSON serialization.

        Returns:
            dict: A dictionary representation of the ChatDTO, including messages.
        """
        return {"chat_id": self.chat_id, "messages": [message.to_dict() for message in self.messages]}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'ChatDTO':
        """
        Constructs a ChatDTO instance from a dictionary.

        Args:
            data (dict): A dictionary containing chat data, including messages.

        Returns:
            ChatDTO: A ChatDTO instance populated with data from the dictionary.
        """
        messages = [MessageDTO.from_dict(message) for message in data["messages"]]
        return ChatDTO(chat_id=data["chat_id"], messages=messages)
