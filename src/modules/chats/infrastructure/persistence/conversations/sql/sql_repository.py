from sqlmodel import Session, select

from .....domain.conversations.interfaces.repository import AbstractConversationRepository
from .....domain.conversations.root import Conversation


class SQLConversationRepository(AbstractConversationRepository):
    def __init__(self, session: Session):
        self.session = session
        self._db_context = DBContext()

    def delete(self, conversation_id: str) -> None:
        """Delete a conversation by its ID."""

        conversation_dset = self._db_context.conversations.delete(conversation_id)

        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = session.exec(statement).one_or_none()
            if result:
                session.delete(result)
                session.commit()

    def find(self, conversation_id: str) -> Conversation:
        """Find a conversation by its ID."""
        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            return session.exec(statement).one_or_none()

    def find_all(self, user_id: str) -> list[Conversation]:
        """Find all conversations for a user."""
        with self.session as session:
            statement = select(Conversation).where(Conversation.owner.id == user_id)
            return session.exec(statement).all()

    def save(self, conversation: Conversation) -> None:
        """Save a conversation."""
        with self.session as session:
            session.add(conversation)
            session.commit()

    def update(self, conversation: Conversation) -> None:
        """Update a conversation."""
        with self.session as session:
            session.add(conversation)
            session.commit()

    def exists(self, conversation_id: str) -> bool:
        """Check if a conversation exists by its ID."""
        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            return session.exec(statement).one_or_none() is not None

    def count(self, user_id: str) -> int:
        """Count the number of conversations for a user."""
        with self.session as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            return session.exec(statement).count()

    def delete_all(self, user_id: str) -> None:
        """Delete all conversations for a user."""
        with self.session as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            results = session.exec(statement).all()
            for result in results:
                session.delete(result)
            session.commit()
