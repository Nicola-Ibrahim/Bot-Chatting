from typing import List

from sqlmodel import Field, Relationship

from src.database.model import Model


class Member(Model, table=True):
    login: str
    first_name: str
    last_name: str
    is_admin: bool = False
    is_owner: bool = False
    conversations: List["Conversation"] = Relationship(back_populates="members")
    messages: List["Message"] = Relationship(back_populates="sender")
