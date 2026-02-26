from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MessageDTO:
    id: str
    sender_id: str
    text: str
    response: str | None
    created_at: datetime | None = None
