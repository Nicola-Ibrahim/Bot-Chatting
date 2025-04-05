from .chats.infrastructure.configuration.startup import ChatStartUp
from .llm_backend.infrastructure.configuration.startup import LLMBackendStartUp


def initialize_module():
    """
    Initialize the module by starting up the necessary components.
    """
    # Initialize the chat startup configuration
    ChatStartUp().initialize()

    # Initialize the LLM backend startup configuration
    LLMBackendStartUp().initialize()
