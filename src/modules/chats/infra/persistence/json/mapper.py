from typing import Any

from ....domain.conversations.root import Conversation
from ....domain.messages.root import Content


class JsonConversationMapper:
    """
    Mapper for converting between Conversation and Content domain models
    and their JSON-serializable representations.
    """

    @staticmethod
    def conversation_to_json(conversation: Conversation) -> dict[str, Any]:
        """
        Converts a Conversation domain model into a JSON-serializable dictionary.

        Args:
            conversation (Conversation): The Conversation domain model.

        Returns:
            dict[str, Any]: JSON-serializable dictionary for the Conversation.
        """
        return {
            "conversation_id": conversation.id,
            "messages": [JsonConversationMapper.prompt_to_json(message) for message in conversation.messages],
        }

    @staticmethod
    def conversation_from_json(data: dict[str, Any]) -> Conversation:
        """
        Converts a JSON dictionary to a Conversation domain model.

        Args:
            data (dict[str, Any]): JSON dictionary with conversation data.

        Returns:
            Conversation: A Conversation domain model populated from the JSON data.
        """
        messages = [JsonConversationMapper.prompt_from_json(prompt_data) for prompt_data in data.get("messages", [])]
        return Conversation(conversation_id=data["conversation_id"], messages=messages)

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
