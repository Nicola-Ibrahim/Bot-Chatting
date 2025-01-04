from dataclasses import dataclass

from src.database.context import DBContext as BaseDBContext

from .conversations.sql.model import Conversation
from .members.model import Member
from .messages.model import Message


@dataclass
class DBContext(BaseDBContext):
    """Manages repositories and session lifecycle for database operations."""

    # Publicly accessible repositories
    conversations: Conversation = Conversation()
    members: Member = Member()
    messages: Message = Message()
