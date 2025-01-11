import uuid
from datetime import datetime, timezone

from sqlmodel import Field, Relationship

from src.database.model import Model


class Message(Model):
    __tablename__ = "messages"

    content: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    # sender_id: uuid.UUID = Field(foreign_key="member.id")
    # sender: "Member" = Relationship(back_populates="messages")
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
