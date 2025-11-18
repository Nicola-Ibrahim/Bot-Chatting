import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from ......database.models import BaseSQLModel


class ConversationDBModel(BaseSQLModel):
    __tablename__ = "conversations"

    # Override default integer PK with UUID string PK
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, default="")
    creator_id = Column(String, ForeignKey("members.id"), nullable=False)
    chat_id = Column(String, nullable=False)
    is_archived = Column(Boolean, default=False)

    members = relationship("MemberDBModel", back_populates="conversations")
    messages = relationship("MessageDBModel", back_populates="conversation")


class MessageDBModel(BaseSQLModel):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sender_id = Column(String, ForeignKey("members.id"))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    feedback = Column(String, nullable=True)
    feedback_timestamp = Column(DateTime, nullable=True)

    sender = relationship("MemberDBModel", back_populates="messages")
    conversation = relationship("ConversationDBModel", back_populates="messages")


class MemberDBModel(BaseSQLModel):
    __tablename__ = "members"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    login = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_creator = Column(Boolean, default=False)

    conversations = relationship("ConversationDBModel", back_populates="members")
    messages = relationship("MessageDBModel", back_populates="sender")
