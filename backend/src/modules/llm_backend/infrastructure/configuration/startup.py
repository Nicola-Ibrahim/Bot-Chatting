from src.paths import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR

from ..processing.document import DocumentProcessor
from .di.containers import (
    LLMBackendContainer,
    LLMDIContainer,  # your DI container for LLM runtime
)

# class LLMsStartUp:
#     """Startup class for the LLM backend module."""

#     def __init__(self):
#         self.container = LLMBackendContainer()

#     def initialize(self) -> None:
#         """Initialize the container and configure the composition root."""

#         DocumentProcessor().preprocess(
#             from_directory=EXTERNAL_DATA_DIR / "optano", to_directory=PROCESSED_DATA_DIR / "preprocessed_data"
#         )

#         self.container.config.from_dict(
#             {
#                 "models": {
#                     "embedding_model_name": "BAAI/bge-small-en-v1.5",
#                     "llm_model_name": "Qwen/Qwen2.5-14B-Instruct",
#                     "llm_tokenizer_name": "Qwen/Qwen2.5-14B-Instruct",
#                     "skip_prompt": True,
#                 },
#                 "search": {
#                     "processed_data_dir": PROCESSED_DATA_DIR / "preprocessed_data",
#                     "top_k": 4,
#                 },
#             }
#         )

#         self.container.init_resources()

#     def shutdown(self):
#         self.container.shutdown_resources()


class LLMsStartUp:
    def __init__(self) -> None:
        self._log = logging.getLogger("llm")
        self._container: LLMDIContainer | None = None

    @property
    def container(self) -> LLMDIContainer:
        if self._container is None:
            raise RuntimeError("LLM container not initialized")
        return self._container

    def initialize(self, config: dict) -> None:
        try:
            self._container = LLMDIContainer()
            # expected: {"default": "...", "providers": {...}}
            self._container.config.from_dict(config)
            self._container.init_resources()
            self._container.wire(
                packages=[
                    "src.contexts.llm_backend.application",
                    "src.contexts.llm_backend.module",
                ]
            )
            self._log.info("LLM module initialized")
        except Exception as ex:
            self._log.exception("LLM initialization failed")
            raise RuntimeError("LLM module bootstrap failed") from ex

    def stop(self) -> None:
        try:
            self._log.info("Shutting down LLM module...")
            if self._container:
                self._container.shutdown_resources()
                self._container.unwire()
        finally:
            self._container = None
