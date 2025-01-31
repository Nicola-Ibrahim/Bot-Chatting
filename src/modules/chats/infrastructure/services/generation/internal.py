from ....domain.messages.interfaces.response_generator import ResponseGenerator


class InternalAIResponseGenerator(ResponseGenerator):
    """
    Implementation of ResponseGenerator that uses an internal AI service.
    """

    def __init__(self, ai_service):
        self.ai_service = ai_service

    def generate_answer(self, text: str) -> str:
        """
        Generates a response using an internal AI service.

        Args:
            text (str): The input text.

        Returns:
            str: The generated response.
        """
        return self.ai_service.generate_response(text)
