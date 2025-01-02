import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel

from ...db_set import DBSet


class Conversation(SQLModel, DBSet, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    chat_id: uuid.UUID = Field(foreign_key="chats.id", nullable=False)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    user: "UsersSQLModel" = Relationship(back_populates="conversations")
    chat: "ChatsSQLModel" = Relationship(back_populates="conversations")
