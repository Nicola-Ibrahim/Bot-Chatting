from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from display.application.use_case.query import DisplayQueryUseCase

from chat.infra.repository.json import JsonFileMemoryRepository

from ..application.services.conversation_service import ConversationApplicationService


class ChatAppDIContainer(containers.DeclarativeContainer):
    # Providers for services
    conversation_download_service = providers.Singleton(ConversationDownloader)
    response_generator = providers.Singleton(AbstractResponseGeneratorService)
    tokenizer = providers.Singleton(AbstractTokenizerService)

    # Providers for repositories
    chat_repo = providers.Singleton(JsonFileMemoryRepository)

    # Wiring up the conversation service
    conversation_service = providers.Factory(
        ConversationApplicationService,
        conversation_download_service=conversation_download_service,
        repository=chat_repo,
        response_generator=response_generator,
        tokenizer=tokenizer,
    )
