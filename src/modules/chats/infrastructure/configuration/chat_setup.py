from .di.chat_backend import ChatDIContainer


class ChatStartUp:
    def __init__(self):
        self._container: ChatDIContainer = None

    @property
    def container(self) -> ChatDIContainer:
        return self._container

    def initialize(self, logger=None) -> None:
        """Initialize the container and configure the composition root."""
        self._container = ChatDIContainer()

        self._container.init_resources()

    # def configure_composition_root(self) -> None:
    #     """Configure the composition root."""

    #     self._container.init_resources()

    def stop(self) -> None:
        """Stop the module and release resources."""
        self._container.shutdown_resources()
