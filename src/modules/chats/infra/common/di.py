from dependency_injector import containers, providers

from ...application.services.conversation_service import ConversationApplicationService
from .. import ConversationDownloader
from .. import JsonFileConversationRepository


class ChatAppDIContainer(containers.DeclarativeContainer):
    conversation_download_service = providers.Singleton(ConversationDownloader)

    repository = providers.Singleton(JsonFileConversationRepository)

    # Wiring up the conversation service
    conversation_service = providers.Factory(
        ConversationApplicationService,
        conversation_download_service=conversation_download_service,
        repository=repository,
    )
