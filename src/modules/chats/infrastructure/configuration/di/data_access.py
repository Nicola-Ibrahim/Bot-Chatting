from dependency_injector import containers, providers

from src.database.conf.manager import DatabaseConnectionManager

from ...persistence.conversations.repository import SQLConversationRepository
from ...persistence.members.repository import SQLMemberRepository
from ...persistence.messages.repository import SQLMessageRepository


class DataAccessDIContainer(containers.DeclarativeContainer):
    """Dependency container for data access layer"""

    config = providers.Configuration()

    database_connection_manager = providers.Singleton(
        DatabaseConnectionManager,
        db_connection_string=config.database.url,
    )

    conversation_repository = providers.Singleton(
        SQLConversationRepository,
        session=database_connection_manager.provided.session,
    )

    member_repository = providers.Singleton(
        SQLMemberRepository,
        session=database_connection_manager.provided.session,
    )

    message_repository = providers.Singleton(
        SQLMessageRepository,
        session=database_connection_manager.provided.session,
    )
