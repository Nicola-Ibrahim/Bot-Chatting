from src.paths import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR

from ..processing.document import DocumentProcessor
from .di.llm_backend import LLMBackendContainer


class LLMBackendStartup:
    """Startup class for the LLM backend module."""

    def __init__(self):
        self.container = LLMBackendContainer()

    def initialize(self) -> None:
        """Initialize the container and configure the composition root."""

        DocumentProcessor().preprocess(
            from_directory=EXTERNAL_DATA_DIR / "optano", to_directory=PROCESSED_DATA_DIR / "preprocessed_data"
        )

        self.container.config.from_dict(
            {
                "models": {
                    "embedding_model_name": "BAAI/bge-small-en-v1.5",
                    "llm_model_name": "Qwen/Qwen2.5-14B-Instruct",
                    "llm_tokenizer_name": "Qwen/Qwen2.5-14B-Instruct",
                    "skip_prompt": True,
                },
                "search": {
                    "processed_data_dir": PROCESSED_DATA_DIR / "preprocessed_data",
                    "top_k": 4,
                },
            }
        )

        self.container.init_resources()

    def shutdown(self):
        self.container.shutdown_resources()
