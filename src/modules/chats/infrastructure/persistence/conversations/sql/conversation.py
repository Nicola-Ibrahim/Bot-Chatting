import uuid

from sqlmodel import Field, Relationship

from src.database.model import BaseModel


class Conversation(BaseModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    members: list["Member"] = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")
