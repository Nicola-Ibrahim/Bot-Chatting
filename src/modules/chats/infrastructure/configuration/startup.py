from logging import Logger

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .di.data_access import DataAccessDIContainer  # SQL database container
from .di.downloader import DownloaderDIContainer  # SQL database container
from .di.email import EmailDIContainer  # Email sender container
from .di.logger import LoggerDIContainer  # Logger container


class ChatDIContainer(containers.DeclarativeContainer):
    """Dependency container for chat bounded context with explicit wiring"""

    config = providers.Configuration()

    logger = providers.Container(LoggerDIContainer)
    email_sender = providers.Container(EmailDIContainer)
    downloader = providers.Container(DownloaderDIContainer)
    data_access = providers.Container(DataAccessDIContainer, config=config.database)

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.chat.application",
            "src.api.modeules",
        ],
    )


class ChatStartUp:
    """Composition root for chat bounded context"""

    def __init__(self, logger: Logger):
        self.logger = logger
        self._container: ChatDIContainer = None

    @property
    def container(self) -> ChatDIContainer:
        if not self._container:
            raise RuntimeError("Container not initialized")
        return self._container

    @inject
    def initialize(
        self, config: dict, db_connection_string: str = Provide[ChatDIContainer.config.database.url]
    ) -> None:
        """Initialize the chat module composition root"""
        try:
            self.logger.info("Initializing chat module dependencies...")

            self._container = ChatDIContainer()
            self._container.config.from_dict(config)

            # Validate dependencies
            self._container.wire()
            self._container.init_resources()

            self.logger.info("Chat module dependencies initialized successfully")

        except Exception as e:
            self.logger.error(f"Chat module initialization failed: {str(e)}")
            raise RuntimeError("Chat module bootstrap failed") from e

    def stop(self) -> None:
        """Clean up resources"""
        try:
            self.logger.info("Shutting down chat module...")
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()

        except Exception as e:
            self.logger.error(f"Chat module shutdown error: {str(e)}")
            raise
        finally:
            self._container = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
