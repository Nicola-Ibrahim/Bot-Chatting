from sqlalchemy import select
from sqlalchemy.orm import Session

from .....domain.conversations.interfaces.repository import AbstractConversationRepository
from .....domain.conversations.root import Conversation


class SQLAlchemyConversationRepository(AbstractConversationRepository):
    def __init__(self, session: Session):
        self.session = session

    def delete(self, conversation_id: str) -> None:
        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = session.execute(statement).scalar_one_or_none()
            if result:
                session.delete(result)
                session.commit()

    def find(self, conversation_id: str) -> Conversation:
        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            return session.execute(statement).scalar_one_or_none()

    def find_all(self, user_id: str) -> list[Conversation]:
        with self.session as session:
            statement = select(Conversation).where(Conversation.owner.id == user_id)
            return session.execute(statement).scalars().all()

    def save(self, conversation: Conversation) -> None:
        with self.session as session:
            session.add(conversation)
            session.commit()

    def update(self, conversation: Conversation) -> None:
        with self.session as session:
            session.add(conversation)
            session.commit()

    def exists(self, conversation_id: str) -> bool:
        with self.session as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            return session.execute(statement).scalar_one_or_none() is not None

    def count(self, user_id: str) -> int:
        with self.session as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            return session.execute(statement).count()

    def delete_all(self, user_id: str) -> None:
        with self.session as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            results = session.execute(statement).scalars().all()
            for result in results:
                session.delete(result)
            session.commit()
