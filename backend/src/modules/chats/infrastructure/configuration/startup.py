import logging
from typing import Self

from .....database.session import SQLAlchemySessionFactory
from .containers import ChatDIContainer

log = logging.getLogger(__name__)


class ChatsStartUp:
    """Composition root for Chats bounded context (self-owned DI container)."""

    def __init__(self) -> None:
        self._container: ChatDIContainer | None = None
        self._session_factory = None
        self._database_url = None

    @property
    def container(self) -> ChatDIContainer:
        if self._container is None:
            raise RuntimeError("Chats container not initialized")
        return self._container

    def initialize(
        self,
        *,
        database_url: str,
        max_active_chats_per_user: int,
    ) -> Self:
        """Create container, load config dict, init resources, wire."""
        if not database_url:
            raise ValueError("Chats configuration requires a 'database_url'")

        self._database_url = database_url

        config = {
            "max_active_chats_per_user": max_active_chats_per_user,
        }

        try:
            self._session_factory = SQLAlchemySessionFactory.acquire(database_url)
            self._container = ChatDIContainer(config=config, session_factory=self._session_factory)

            # Order: init resources, then wire packages using Provide[...] markers
            self._container.init_resources()

            return self
        except Exception as ex:
            raise RuntimeError("Chats module bootstrap failed") from ex

    def stop(self) -> None:
        """Graceful shutdown."""
        try:
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            if self._database_url:
                SQLAlchemySessionFactory.release(self._database_url)
            self._container = None
