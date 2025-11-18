import logging

from dependency_injector import containers, providers

from ..mediator import Mediator
from ..persistence.repositories.sql_conversation_repo import SQLConversationRepository
from ..persistence.repositories.sql_message_repo import SQLMessageRepository

# Handler registry placeholder; wire concrete handlers here.
handlers: dict = {}


class LoggerDIContainer(containers.DeclarativeContainer):
    logger = providers.Singleton(logging.getLogger, name="chat")


class RepositoryDIContainer(containers.DeclarativeContainer):
    """Dependency container for data access layer"""

    config = providers.Configuration()

    db = providers.DependenciesContainer()  # expects: session (Factory) or session_factory

    # Repositories receive DB session or factory from the external DB container
    conversation_repository = providers.Factory(
        SQLConversationRepository,
        session=db.provided.session,
    )
    message_repository = providers.Factory(SQLMessageRepository, session=db.provided.session)


class ChatDIContainer(containers.DeclarativeContainer):
    """Dependency container for chat bounded context with explicit wiring"""

    config = providers.Configuration()

    logger = providers.Container(LoggerDIContainer)
    repository = providers.Container(RepositoryDIContainer, config=config.database)

    # Build mediator with all command/query handlers (feature-first)
    mediator = providers.Singleton(Mediator, handlers=handlers)

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.backend.modules.chats.application",
        ],
    )
