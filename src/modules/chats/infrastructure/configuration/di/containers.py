import logging

from dependency_injector import containers, providers

from src.database.configuration.manager import DatabaseConnectionManager

from ....application import ConversationApplicationService
from ... import ConversationDownloader, ConversationsDownloader, EmailSender, JsonFileConversationRepository
from ...persistence.conversations.repository import SQLConversationRepository
from ...persistence.members.repository import SQLMemberRepository
from ...persistence.messages.repository import SQLMessageRepository


class LoggerDIContainer(containers.DeclarativeContainer):
    logger = providers.Singleton(logging.getLogger, name="chat")


class EmailDIContainer(containers.DeclarativeContainer):
    email_sender = providers.Singleton(EmailSender)


class ConversationDIContainer(containers.DeclarativeContainer):
    conversation_download_service = providers.Singleton(ConversationDownloader)

    repository = providers.Singleton(JsonFileConversationRepository)

    # Wiring up the conversation service
    conversation_service = providers.Factory(
        ConversationApplicationService,
        conversation_download_service=conversation_download_service,
        repository=repository,
    )


class DownloaderDIContainer(containers.DeclarativeContainer):
    conversation_download_service = providers.Singleton(ConversationsDownloader)


class DataAccessDIContainer(containers.DeclarativeContainer):
    """Dependency container for data access layer"""

    config = providers.Configuration()

    db = providers.DependenciesContainer()  # expects: session (Factory) or session_factory

    # Repositories receive DB session or factory from the external DB container
    conversation_repository = providers.Factory(
        SQLConversationRepository,
        session=db.provided.session,  # provided by DatabaseContainer
    )
    member_repository = providers.Factory(SQLMemberRepository, session=db.provided.session)
    message_repository = providers.Factory(SQLMessageRepository, session=db.provided.session)


class ChatDIContainer(containers.DeclarativeContainer):
    """Dependency container for chat bounded context with explicit wiring"""

    config = providers.Configuration()

    logger = providers.Container(LoggerDIContainer)
    email_sender = providers.Container(EmailDIContainer)
    downloader = providers.Container(DownloaderDIContainer)
    data_access = providers.Container(DataAccessDIContainer, config=config.database)

    # Build mediator with all command/query handlers (feature-first)
    handlers = providers.Factory(build_handlers_registry)
    mediator = providers.Singleton(Mediator, handlers=handlers)

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.chat.application",
        ],
    )
