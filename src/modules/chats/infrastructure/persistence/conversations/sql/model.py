import uuid

from sqlmodel import Field, Relationship

from src.database.model import Model


class Conversation(Model, table=True):
    __tablename__ = "conversations"

    title: str
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    chat_id: uuid.UUID = Field(foreign_key="chats.id", nullable=False)
    members: list["Member"] = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")
