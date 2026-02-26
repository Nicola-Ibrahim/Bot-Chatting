from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ConversationStartedDTO:
    conversation_id: str
    title: str
