from typing import Iterable, Optional

from ....domain.messages.interfaces.repository import AbstractMessageRepository
from ....domain.messages.root import Message


class SQLMessageRepository(AbstractMessageRepository):
    """Placeholder SQL repository for messages."""

    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def get_by_id(self, message_id: str) -> Optional[Message]:
        # TODO: implement persistence lookup
        raise NotImplementedError

    def list_for_conversation(self, conversation_id: str) -> Iterable[Message]:
        # TODO: implement persistence lookup
        raise NotImplementedError

    def save(self, message: Message) -> None:
        # TODO: implement persistence save
        raise NotImplementedError

    def update(self, message: Message) -> None:
        # TODO: implement persistence update
        raise NotImplementedError

    def delete(self, message_id: str) -> None:
        # TODO: implement persistence delete
        raise NotImplementedError
