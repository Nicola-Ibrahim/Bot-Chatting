from dependency_injector import containers, providers

from src.chat.infra.di import ChatAppDIContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.chat.presentation.web.api",
        ]
    )

    chat = providers.Container(ChatAppDIContainer)
