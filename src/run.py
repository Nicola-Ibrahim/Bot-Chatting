from src.api.app import ChatbotFastAPIApp
from src.modules.chats.infrastracture.configuration.chat_startup import ChatStartUp
from src.modules.llm_backend.infrastructure.configuration.llm_backend_startup import LLMBackendStartup


def initialize_application_components():
    """Initializes and configures the core application components."""
    llm_backend_startup = LLMBackendStartup()
    llm_backend_startup.initialize()

    chat_startup = ChatStartUp()
    chat_startup.initialize()


def create_and_run_api():
    """Creates and runs the Flask application."""
    ChatbotFastAPIApp.start()


def main():
    """Main entry point: Initializes DI and runs the app."""
    initialize_application_components()
    create_and_run_api()


if __name__ == "__main__":
    main()
