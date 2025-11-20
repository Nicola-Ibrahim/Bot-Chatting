import logging

from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from ..mediator import Mediator
from ..persistence.repositories.sql_conversation_repo import SQLConversationRepository
from ..persistence.repositories.sql_message_repo import SQLMessageRepository

# Handler registry placeholder; wire concrete handlers here.
handlers: dict = {}


class ChatDIContainer(containers.DeclarativeContainer):
    """Top-level Chats BC container."""

    config = providers.Configuration()
    session_factory = providers.Dependency(instance_of=sessionmaker)

    logger = providers.Singleton(logging.getLogger, name="chat")

    conversation_repository = providers.Factory(
        SQLConversationRepository,
        session_factory=session_factory,
    )

    message_repository = providers.Factory(
        SQLMessageRepository,
        session_factory=session_factory,
    )

    mediator = providers.Singleton(Mediator, handlers=handlers)

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.backend.modules.chats.application",
        ],
    )
