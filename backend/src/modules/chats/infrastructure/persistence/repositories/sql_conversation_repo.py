import uuid
from typing import Callable, Iterable, Optional

from sqlalchemy import delete as sqla_delete
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ....domain.conversations.conversation import Conversation
from ....domain.conversations.value_objects.conversation_id import ConversationId
from ....domain.interfaces.conversation_repository import BaseConversationRepository
from ....domain.members.value_objects.member_id import MemberId
from ..orm.model import ConversationDBModel


def map_to_entity(row: ConversationDBModel) -> Conversation:
    """Map a database row to a domain aggregate."""
    if row is None:
        return None
    creator_id = MemberId.create(row.creator_id)
    # TODO: Prefer a rehydrate constructor that does not raise domain events.
    conversation = Conversation.create(creator_id=creator_id, creator_name="", title=row.title)
    conversation._id = ConversationId.create(uuid.UUID(str(row.id)))  # re-use persisted id
    conversation._is_archived = row.is_archived  # re-use persisted archived flag
    return conversation


def map_to_db(entity: Conversation) -> ConversationDBModel:
    """Map a domain aggregate to its persistence representation."""
    return ConversationDBModel(
        id=str(entity.id),
        title=entity.title,
        creator_id=str(entity.creator.id.value),
        chat_id=str(entity.id),
        is_archived=entity.is_archived,
    )


class SQLConversationRepository(BaseConversationRepository):
    """SQL-based repository using an injected SQLAlchemy Session."""

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory

    # ---------- Queries ----------

    def find(self, conversation_id: str) -> Conversation:
        with self._session_factory() as session:
            row = session.get(ConversationDBModel, str(conversation_id))
            return map_to_entity(row)

    def find_all(self, user_id: str) -> list[Conversation]:
        # If your column is named creator_id in the DB model, filter by that.
        stmt = select(ConversationDBModel).where(ConversationDBModel.creator_id == str(user_id))
        with self._session_factory() as session:
            rows = session.execute(stmt).scalars().all()
            return [c for c in (map_to_entity(r) for r in rows) if c is not None]

    def exists(self, conversation_id: str) -> bool:
        with self._session_factory() as session:
            return session.get(ConversationDBModel, str(conversation_id)) is not None

    def count(self, user_id: str) -> int:
        stmt = (
            select(func.count()).select_from(ConversationDBModel).where(ConversationDBModel.creator_id == str(user_id))
        )
        with self._session_factory() as session:
            return int(session.execute(stmt).scalar_one())

    # ---------- Commands ----------

    def save(self, conversation: Conversation) -> None:
        with self._session_factory() as session:
            session.add(map_to_db(conversation))
            session.commit()

    def update(self, conversation: Conversation) -> None:
        with self._session_factory() as session:
            session.merge(map_to_db(conversation))
            session.commit()

    def delete(self, conversation_id: str) -> None:
        with self._session_factory() as session:
            row = session.get(ConversationDBModel, str(conversation_id))
            if not row:
                raise ValueError(f"Conversation with ID {conversation_id} does not exist.")
            session.delete(row)
            session.commit()

    def delete_all(self, user_id: str) -> None:
        # Bulk delete; if you need per-row hooks, load then delete.
        stmt = sqla_delete(ConversationDBModel).where(ConversationDBModel.creator_id == str(user_id))
        with self._session_factory() as session:
            session.execute(stmt)
            session.commit()
