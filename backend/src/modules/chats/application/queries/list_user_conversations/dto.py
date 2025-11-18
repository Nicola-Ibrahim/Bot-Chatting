from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ConversationSummaryDTO:
    id: str
    title: str
    is_archived: bool
