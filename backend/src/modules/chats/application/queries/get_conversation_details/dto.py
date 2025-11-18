from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True, frozen=True)
class ConversationDetailsDTO:
    id: str
    title: str
    is_archived: bool
    creator_id: str | None = None
    participants: Tuple[dict, ...] = ()
