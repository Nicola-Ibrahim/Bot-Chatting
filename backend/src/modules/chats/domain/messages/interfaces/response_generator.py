from abc import ABC, abstractmethod


class ResponseGenerator(ABC):
    """
    Abstract base class for generating responses.
    """

    @abstractmethod
    def generate_answer(self, text: str) -> str:
        """
        Generates a response based on the input text.

        Args:
            text (str): The input text.

        Returns:
            str: The generated response.
        """
        raise NotImplementedError
