from typing import Any

from ....domain.entities.conversation import Chat
from ....domain.entities.message import Content


class JsonChatMapper:
    """
    Mapper for converting between Chat and Content domain models
    and their JSON-serializable representations.
    """

    @staticmethod
    def chat_to_json(chat: Chat) -> dict[str, Any]:
        """
        Converts a Chat domain model into a JSON-serializable dictionary.

        Args:
            chat (Chat): The Chat domain model.

        Returns:
            dict[str, Any]: JSON-serializable dictionary for the Chat.
        """
        return {"chat_id": chat.id, "messages": [JsonChatMapper.prompt_to_json(message) for message in chat.messages]}

    @staticmethod
    def chat_from_json(data: dict[str, Any]) -> Chat:
        """
        Converts a JSON dictionary to a Chat domain model.

        Args:
            data (dict[str, Any]): JSON dictionary with chat data.

        Returns:
            Chat: A Chat domain model populated from the JSON data.
        """
        messages = [JsonChatMapper.prompt_from_json(prompt_data) for prompt_data in data.get("messages", [])]
        return Chat(chat_id=data["chat_id"], messages=messages)

    @staticmethod
    def prompt_to_json(message: Content) -> dict[str, Any]:
        """
        Converts a Content domain model to a JSON-serializable dictionary.

        Args:
            message (Content): The Content domain model.

        Returns:
            dict[str, Any]: JSON-serializable dictionary for the Content.
        """
        return {"id": message.id, "question": message.text, "answer": message.response}

    @staticmethod
    def prompt_from_json(data: dict[str, Any]) -> Content:
        """
        Converts a JSON dictionary to a Content domain model.

        Args:
            data (dict[str, Any]): JSON dictionary with message data.

        Returns:
            Content: A Content domain model populated from the JSON data.
        """
        return Content(id=data["id"], text=data["text"], response=data.get("response"))
