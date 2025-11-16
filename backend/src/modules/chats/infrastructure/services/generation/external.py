import requests

from ....domain.messages.interfaces.response_generator import ResponseGenerator


class ExternalAPIResponseGenerator(ResponseGenerator):
    """
    Implementation of ResponseGenerator that uses an external API.
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def generate_answer(self, text: str) -> str:
        """
        Generates a response using an external API.

        Args:
            text (str): The input text.

        Returns:
            str: The generated response.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"text": text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()["answer"]
