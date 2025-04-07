from dependency_injector import containers, providers

from src.modules.chats.infrastructure.chat_module import ChatsModule


class MeetingsModuleDIContainer(containers.DeclarativeContainer):
    """Dependency Injection container for the meetings module"""

    meetings_module = providers.Factory(ChatsModule)
