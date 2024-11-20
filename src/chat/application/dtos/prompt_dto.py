from dataclasses import dataclass, field
from typing import Any


@dataclass
class MessageDTO:
    """Data Transfer Object for representing a single message within a chat session."""

    id: str
    question: str
    answer: str = None

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the MessageDTO instance into a dictionary format for JSON serialization.

        Returns:
            dict: A dictionary representation of the MessageDTO.
        """
        return {"id": self.id, "question": self.question, "answer": self.answer}

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'MessageDTO':
        """
        Constructs a MessageDTO instance from a dictionary.

        Args:
            data (dict): A dictionary containing message data.

        Returns:
            MessageDTO: A MessageDTO instance populated with data from the dictionary.
        """
        return MessageDTO(id=data["id"], question=data["question"], answer=data.get("answer"))
