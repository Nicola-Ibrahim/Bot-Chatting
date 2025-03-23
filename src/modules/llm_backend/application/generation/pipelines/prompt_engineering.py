from typing import Any

from dependency_injector.wiring import Provide, inject

from ...infrastructure.configuration.di.llm_backend import LLMBackendContainer
from ...infrastructure.processing.typedefs import LlmModel, Tokenizer


class TextProcessor:
    """Handles all text transformation operations including tokenization and detokenization"""

    @inject
    def __init__(
        self,
        tokenizer: Tokenizer = Provide[LLMBackendContainer.models.tokenizer],
        language_model: LlmModel = Provide[LLMBackendContainer.models.llm_model],
    ):
        """
        Args:
            tokenizer: Text tokenizer instance
            language_model: Language model for device configuration
        """
        self.tokenizer = tokenizer
        self.device = language_model.device

    def tokenize_for_model(self, text: str) -> Any:
        """Tokenizes and formats text for model input"""
        try:
            return self.tokenizer([text], return_tensors="pt", padding=True, truncation=True).to(self.device)
        except Exception as e:
            raise ValueError(f"Input tokenization failed: {str(e)}") from e

    def decode_model_output(self, tokenized_input: Any, generated_response: Any) -> str:
        """Decodes model outputs to text with input context trimming"""
        try:
            trimmed_ids = [
                output[len(input) :] for input, output in zip(tokenized_input.input_ids, generated_response)
            ]
            return self.tokenizer.batch_decode(trimmed_ids, skip_special_tokens=True)[0]
        except Exception as e:
            raise ValueError(f"Output decoding failed: {str(e)}") from e


class PromptFormatter:
    """End-to-end input processor for Qwen model - handles document context preparation and prompt formatting"""

    @inject
    def __init__(
        self, tokenizer: Tokenizer = Provide[LLMBackendContainer.models.tokenizer], max_docs_for_context: int = 1
    ):
        """
        Args:
            tokenizer: HF tokenizer for Qwen model
            max_docs_for_context: Maximum documents to include in context
        """
        self.tokenizer = tokenizer
        self.max_docs_for_context = max_docs_for_context

    def _build_context_from_docs(self, context_docs: list[tuple[str, str, Any]]) -> str:
        """Processes and cleans document content for context"""
        if not context_docs:
            return ""

        selected = context_docs[: self.max_docs_for_context]
        return "\n\n".join(
            f"Document {doc_index + 1} ({path}):\n{content.replace('\n\n\n', '\n\n').strip()}"
            for doc_index, (path, content, _) in enumerate(selected)
        )

    def _create_chat_template(self, user_query: str, context: str) -> str:
        """Generates Qwen-specific chat template"""
        return self.tokenizer.apply_chat_template(
            conversation=[
                {
                    "role": "system",
                    "content": "This is a chat between a user and an artificial intelligence assistant working for Optano. "
                    "The assistant gives helpful, detailed, and polite answers to the user’s questions "
                    "based on the context. The assistant should also indicate when the answer cannot be "
                    "found in the context. In this case, the assistant answers with 'I cannot help you answering this question based on the documentation.'. It gives a full and complete answer for the question and include image paths from the context."
                    "The assistant answers with the correct Latex Code using $...$ for short formulas and $$...$$ for longer formulas.",
                },
                {"role": "system", "content": context},
                {"role": "user", "content": user_query},
            ],
            tokenize=False,  # Ensure this parameter is set to False, to avoid tokenizing the prompt
            add_generation_prompt=True,  # Enusre this pararmeter is set to True, to format the prompt in way that the model can understand as chat rather than just continuation of the context, so that the model can generate a response
        )

    def format(self, user_query: str, context_docs: list[tuple[str, str, Any]]) -> str:
        """Complete processing pipeline from raw inputs to model-ready format"""
        context = self._build_context_from_docs(context_docs)
        return self._create_chat_template(user_query, context)
