from abc import ABC

import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import AutoModelForCausalLM


class BaseModel(ABC):
    """Abstract base class for models that generate responses based on messages and context."""

    pass


class LlmModel(BaseModel):
    """Proxy class for interacting with the Llama model from HuggingFace."""

    _instance = None

    def __new__(cls, model_name: str = None):
        if cls._instance is None:
            # Directly instantiate the base HuggingFace model
            model_name = model_name or "nvidia/Llama3-ChatQA-2-8B"
            cls._instance = AutoModelForCausalLM.from_pretrained(
                model_name, torch_dtype=torch.float16, device_map="auto"
            )
        return cls._instance

    def __init__(self, model_name: str = None) -> None:
        # No need to reinitialize; the base model is already initialized in __new__
        pass


class HuggingFaceLargeLanguageModel(BaseModel):
    """Proxy class for interacting with the LLM from HuggingFace."""

    _instance = None

    def __new__(cls, llm_model_name: str = None):
        if cls._instance is None:
            # Directly instantiate the base HuggingFace LLM model
            llm_model_name = llm_model_name or "HuggingFaceH4/zephyr-7b-alpha"
            cls._instance = HuggingFaceLLM(model_name=llm_model_name)
        return cls._instance

    def __init__(self, llm_model_name: str = None) -> None:
        # No need to reinitialize; the base model is already initialized in __new__
        pass


class EmbeddingModel(BaseModel):
    """Proxy class for interacting with the embedding model from HuggingFace."""

    _instance = None

    def __new__(cls, embedding_model_name: str = None):
        if cls._instance is None:
            # Directly instantiate the base HuggingFace embedding model
            embedding_model_name = embedding_model_name or "BAAI/bge-small-en-v1.5"
            cls._instance = HuggingFaceEmbedding(model_name=embedding_model_name)
        return cls._instance

    def __init__(self, embedding_model_name: str = None) -> None:
        # No need to reinitialize; the base model is already initialized in __new__
        pass
