from typing import Any

from dependency_injector.wiring import Provide, inject
from transformers import TextStreamer

from ...infrastructure.configuration.di.llm_backend import LLMBackendContainer
from ...infrastructure.processing.typedefs import LlmModel


class ResponseGenerator:
    """Abstract base class for LLM response generation."""

    @inject
    def __init__(
        self,
        language_model: LlmModel = Provide[LLMBackendContainer.models.llm_model],
    ) -> None:
        """Initializes the ResponseGenerator with essential components.

        Args:
            language_model: The core language model for text generation
        """
        self.language_model = language_model
        self.default_temperature = 0.6

    def generate(
        self,
        model_inputs: Any,
        temperature: float,
        streamer: TextStreamer | None = None,
    ) -> Any:
        """Generates responses with configured parameters.

        Args:
            model_inputs: Preprocessed model inputs (tokenized + formatted)
            temperature: Creativity control parameter
            streamer: Optional streaming interface

        Returns:
            Model's raw output for downstream processing
        """

        return self.language_model.generate(
            **model_inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=temperature or self.default_temperature,
            streamer=streamer,
        )
