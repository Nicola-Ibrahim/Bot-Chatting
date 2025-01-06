import uuid
from datetime import datetime, timezone

from sqlmodel import Field, Relationship

from src.database.model import Model


class Message(Model):
    __tablename__ = "messages"

    content: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    sender_id: uuid.UUID = Field(foreign_key="member.id")
    conversation: "Conversation" = Relationship(back_populates="messages")
    sender: "Member" = Relationship(back_populates="messages")
