import torch
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoModelForCausalLM, AutoTokenizer

from .typedefs import EmbeddingModel, LlmModel, Tokenizer


class ModelLoader:
    """A class responsible for loading Hugging Face models (LLMs, embeddings)."""

    @staticmethod
    def load_llm_model(
        model_name: str,
        device_map: str | None = "auto",
        torch_dtype: torch.dtype | None = torch.float16,
    ) -> LlmModel:
        """Loads a Large Language Model (LLM) from Hugging Face.

        Args:
            model_name: The name or path of the pre-trained model.
            device_map: The device mapping for the model ("auto" or specific device).
            torch_dtype: The torch data type for the model.

        Returns:
            The loaded LLM model.
        """

        return AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_dtype, device_map=device_map)

    @staticmethod
    def load_embedding_model(model_name: str) -> EmbeddingModel:
        """Loads an embedding model from Hugging Face.

        Args:
            model_name: The name or path of the pre-trained model.

        Returns:
            The loaded embedding model.
        """
        return HuggingFaceEmbedding(model_name=model_name)


class TokenizerLoader:
    """A class responsible for loading Hugging Face tokenizers."""

    @staticmethod
    def load_tokenizer(model_name: str) -> Tokenizer:
        """Loads a Hugging Face tokenizer.

        Args:
            model_name: The name or path of the pre-trained model (tokenizer is inferred from this).

        Returns:
            The loaded tokenizer.
        """
        return AutoTokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
