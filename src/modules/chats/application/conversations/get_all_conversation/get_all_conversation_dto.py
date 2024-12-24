import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetAllConversationsDTO:
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

    @classmethod
    def from_domain(cls, conversation):
        return cls(id=conversation.id, user_id=conversation.user_id, created_at=conversation.created_at)
