import uuid

from sqlmodel import Field, Relationship

from ......database.models import BaseSQLModel


class ConversationDBModel(BaseSQLModel):
    __tablename__ = "conversations"

    id: int = Field(primary_key=True)
    title: str = Field(default="")
    creator_id: uuid.UUID = Field(foreign_key="members.id", nullable=False)
    chat_id: uuid.UUID = Field(foreign_key="chats.id", nullable=False)
    is_archived: bool = Field(default=False)
    members: list["Member"] = Relationship(back_populates="conversations")
    messages: list["MessageDBModel"] = Relationship(back_populates="conversation")
    participants: list["ParticipantDBModel"] = Relationship(back_populates="conversation")

    # If you need a direct mapping between message ids and participants
    # you could use a normalized table for participants and messages
