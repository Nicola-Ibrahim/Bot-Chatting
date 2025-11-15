from sqlalchemy import delete as sqla_delete
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ....domain.conversations.interfaces.repository import BaseRepository
from ....domain.conversations.root import Conversation
from ....domain.conversations.value_objects.conversation_id import ConversationId
from ....domain.members.value_objects.member_id import MemberId
from .model import ConversationDBModel


def map_to_entity(row: ConversationDBModel) -> Conversation:
    """Map a database row to a domain aggregate."""
    if row is None:
        return None
    creator_id = MemberId.create(row.creator_id)
    # TODO: Prefer a rehydrate constructor that does not raise domain events.
    conversation = Conversation.create(creator_id=creator_id, creator_name="", title=row.title)
    conversation._id = ConversationId.create(row.id)  # re-use persisted id
    conversation._is_archived = row.is_archived  # re-use persisted archived flag
    return conversation


def map_to_db(entity: Conversation) -> ConversationDBModel:
    """Map a domain aggregate to its persistence representation."""
    return ConversationDBModel(
        id=entity.id,
        title=entity.title,
        creator_id=entity.creator.id.value,
        chat_id=entity.id,
        is_archived=entity.is_archived,
    )


class SQLConversationRepository(BaseRepository):
    """SQL-based repository using an injected SQLAlchemy Session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    # ---------- Queries ----------

    def find(self, conversation_id: str) -> Conversation:
        row = self._session.get(ConversationDBModel, conversation_id)
        return map_to_entity(row)

    def find_all(self, user_id: str) -> list[Conversation]:
        # If your column is named creator_id in the DB model, filter by that.
        stmt = select(ConversationDBModel).where(ConversationDBModel.creator_id == user_id)
        rows = self._session.execute(stmt).scalars().all()
        return [c for c in (map_to_entity(r) for r in rows) if c is not None]

    def exists(self, conversation_id: str) -> bool:
        return self._session.get(ConversationDBModel, conversation_id) is not None

    def count(self, user_id: str) -> int:
        stmt = select(func.count()).select_from(ConversationDBModel).where(ConversationDBModel.creator_id == user_id)
        return int(self._session.execute(stmt).scalar_one())

    # ---------- Commands ----------

    def save(self, conversation: Conversation) -> None:
        self._session.add(map_to_db(conversation))

    def update(self, conversation: Conversation) -> None:
        self._session.merge(map_to_db(conversation))

    def delete(self, conversation_id: str) -> None:
        row = self._session.get(ConversationDBModel, conversation_id)
        if not row:
            raise ValueError(f"Conversation with ID {conversation_id} does not exist.")
        self._session.delete(row)

    def delete_all(self, user_id: str) -> None:
        # Bulk delete; if you need per-row hooks, load then delete.
        stmt = sqla_delete(ConversationDBModel).where(ConversationDBModel.creator_id == user_id)
        self._session.execute(stmt)
