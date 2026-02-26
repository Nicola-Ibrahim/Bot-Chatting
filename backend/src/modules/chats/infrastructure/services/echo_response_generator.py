from src.modules.chats.domain.messages.interfaces.response_generator import ResponseGenerator


class EchoResponseGenerator(ResponseGenerator):
    """Simple fallback response generator when none is configured."""

    def generate_answer(self, text: str) -> str:
        return text
