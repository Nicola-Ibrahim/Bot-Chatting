from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SentMessageDTO:
    message_id: str
    conversation_id: str
    sender_id: str
