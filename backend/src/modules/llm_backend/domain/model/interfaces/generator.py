from abc import ABC, abstractmethod
from typing import Any, Dict


class ModelGenerator(ABC):
    """
    Abstract base class for model services.
    """

    @abstractmethod
    def generate_response(self, input_text: str, **kwargs) -> str:
        """
        Generates a response based on the input text.

        Args:
            input_text (str): The input text.
            **kwargs: Additional model-specific parameters.

        Returns:
            str: The generated response.
        """
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self) -> ModelMetadata:
        """
        Returns metadata about the model.

        Returns:
            ModelMetadata: Metadata about the model.
        """
        raise NotImplementedError
