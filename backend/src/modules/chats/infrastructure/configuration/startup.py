from .di.containers import ChatDIContainer


class ChatsStartUp:
    """Composition root for Chats bounded context (self-owned DI container)."""

    def __init__(self) -> None:
        self._container: ChatDIContainer | None = None

    @property
    def container(self) -> ChatDIContainer:
        if self._container is None:
            raise RuntimeError("Chats container not initialized")
        return self._container

    def initialize(self, config: dict) -> None:
        """Create container, load config dict, init resources, wire."""
        try:
            self._container = ChatDIContainer()
            # expected: {"database": {"url": "..."}}
            self._container.config.from_dict(config)

            # Order: init resources, then wire packages using Provide[...] markers
            self._container.init_resources()
            self._container.wire(
                packages=[
                    "src.contexts.chats.application",  # handlers, services using @inject/Provide
                    "src.contexts.chats.module",  # if you expose a ChatsModule facade
                ]
            )

        except Exception as ex:
            raise RuntimeError("Chats module bootstrap failed") from ex

    def stop(self) -> None:
        """Graceful shutdown."""
        try:
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            self._container = None
