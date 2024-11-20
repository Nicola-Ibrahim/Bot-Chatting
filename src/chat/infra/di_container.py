from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from display.application.use_case.query import DisplayQueryUseCase

from chat.infra.repository.json import JsonFileMemoryRepository


class ChatDIContainer(containers.DeclarativeContainer):
    chat_repo = providers.Factory(JsonFileMemoryRepository)
