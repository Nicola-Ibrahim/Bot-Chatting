from sqlmodel import Relationship

from src.database.model import Model


class Member(Model):
    __tablename__ = "members"

    login: str
    first_name: str
    last_name: str
    is_admin: bool = False
    is_creator: bool = False
    conversations: list["Conversation"] = Relationship(back_populates="members")
    messages: list["Message"] = Relationship(back_populates="sender")
