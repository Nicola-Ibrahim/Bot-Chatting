from .chats.infrastructure.configuration.startup import ChatsStartUp
from .llm_backend.infrastructure.configuration.startup import LLMsStartUp


def initialize_modules():
    """
    Initialize the module by starting up the necessary components.
    """
    ChatsStartUp.initialize()

    LLMsStartUp.initialize()

    UsersStartUp.initialize()
