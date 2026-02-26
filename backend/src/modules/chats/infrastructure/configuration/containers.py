from dependency_injector import containers, providers

from ...application.conversation_lifecycle.service import ConversationLifecycleService
from ...application.membership.service import MembershipService
from ...application.messaging.service import MessagingService
from ...application.queries.service import ChatQueryService
from ..persistence.repositories.sql_conversation_repo import SQLConversationRepository
from ..persistence.repositories.sql_message_repo import SQLMessageRepository
from ..services.echo_response_generator import EchoResponseGenerator


class ChatDIContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_factory = providers.Dependency()

    conversation_repository = providers.Resource(
        SQLConversationRepository,
        session_factory=session_factory,
    )

    message_repository = providers.Resource(
        SQLMessageRepository,
        session_factory=session_factory,
    )

    response_generator = providers.Resource(
        EchoResponseGenerator,
    )

    conversation_lifecycle_service = providers.Factory(
        ConversationLifecycleService,
        conversation_repository=conversation_repository,
    )

    membership_service = providers.Factory(
        MembershipService,
        conversation_repository=conversation_repository,
    )

    messaging_service = providers.Factory(
        MessagingService,
        messages_repository=message_repository,
        response_generator=response_generator,
    )

    chat_query_service = providers.Factory(
        ChatQueryService,
        conversation_repository=conversation_repository,
        messages_repository=message_repository,
    )

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.modules.chats.application",
        ],
    )
