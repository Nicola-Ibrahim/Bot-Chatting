from dependency_injector import containers, providers

from ...processing.context import MemoryManager
from ...processing.feedback import FileFeedbackManager
from .service import ServiceDIContainer


class ChatDIContainer(containers.DeclarativeContainer):
    """Main container for the chat module."""

    services = providers.Container(ServiceDIContainer)

    memory_manager = providers.Factory(
        MemoryManager,
        memory_file="chat_memory",
        token_limit=500,
        max_recent=5,
    )

    feed_back_manager = providers.Factory(
        FileFeedbackManager,
        file_name="feedbacks",
    )
    wiring_config = containers.WiringConfiguration(
        modules=["src.web.chat.endpoints"],
        packages=[
            "src.chat.application",
        ],
    )
