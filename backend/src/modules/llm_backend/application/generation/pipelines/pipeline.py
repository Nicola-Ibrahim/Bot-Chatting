from typing import Any

from src.building_blocks.infrastructure.pipeline import Pipeline, PipelineExecutionError, PipelineStage
from src.llm_backend.application.prompt.context import DocumentFetcher
from src.llm_backend.application.prompt.generation import ResponseGenerator
from src.llm_backend.application.prompt.prompt_engineering import PromptFormatter, TextProcessor
from src.llm_backend.application.prompt.response_formatting import ResponseFormatter
from src.llm_backend.application.prompt.response_validation import ResponseValidator


class ContextDocumentFetcherStage(PipelineStage):
    """Fetches relevant context documents based on the input prompt."""

    def __init__(self) -> None:
        self.document_fetcher = DocumentFetcher()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            query_text = data["prompt"]
            context_identifier = data.get("prompt_id")
            fetched_documents = self.document_fetcher.retrieve_documents(
                query=query_text, context_id=context_identifier
            )
            data["fetched_documents"] = fetched_documents
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Document fetching failed: {str(e)}"
            ) from e


class AugmentedPromptFormatterStage(PipelineStage):
    """Formats the prompt by incorporating retrieved context documents for LLM processing."""

    def __init__(self):
        self.prompt_formatter = PromptFormatter()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            user_query = data["prompt"]
            context_docs = data["fetched_documents"]
            enriched_prompt = self.prompt_formatter.format(user_query=user_query, context_docs=context_docs)
            data["enriched_prompt"] = enriched_prompt
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Prompt formatting failed: {str(e)}"
            ) from e


class ModelInputTokenizerStage(PipelineStage):
    """Tokenizes the enriched prompt for the LLM model."""

    def __init__(self):
        self.text_processor = TextProcessor()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            enriched_prompt = data["enriched_prompt"]
            tokenized_input = self.text_processor.tokenize_for_model(enriched_prompt)
            data["tokenized_input"] = tokenized_input
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Tokenization failed: {str(e)}"
            ) from e


class LLMResponseGeneratorStage(PipelineStage):
    """Generates a response from the LLM based on the tokenized input."""

    def __init__(self):
        self.llm_response_generator = ResponseGenerator()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            tokenized_input = data["tokenized_input"]
            generated_response = self.llm_response_generator.generate(
                model_inputs=tokenized_input,
                temperature=data.get("temperature", 0.6),
                streamer=data.get("streamer"),
            )
            data["generated_response"] = generated_response
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"LLM response generation failed: {str(e)}"
            ) from e


class ResponseDecoderStage(PipelineStage):
    """Decodes the LLM's tokenized output into human-readable text."""

    def __init__(self):
        self.text_processor = TextProcessor()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            tokenized_input = data["tokenized_input"]
            generated_response = data["generated_response"]
            decoded_response = self.text_processor.decode_model_output(
                tokenized_input=tokenized_input, generated_response=generated_response
            )
            data["decoded_response"] = decoded_response
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Response decoding failed: {str(e)}"
            ) from e


class ResponsePostProcessorStage(PipelineStage):
    """Post-processes the decoded response to produce a final formatted answer."""

    def __init__(self):
        self.response_formatter = ResponseFormatter()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            decoded_response = data["decoded_response"]
            formatted_final_response = self.response_formatter.format(raw_response=decoded_response)
            data["formatted_final_response"] = formatted_final_response
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Response post-processing failed: {str(e)}"
            ) from e


class ResponseAccuracyValidatorStage(PipelineStage):
    """Validates the accuracy and relevance of the LLM's generated response."""

    def __init__(self) -> None:
        self.response_validator = ResponseValidator()

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        try:
            generated_response = data["decoded_response"]
            context_docs = data["fetched_documents"]
            validation_threshold = data.get("validation", 0.85)

            sentences, similarity_scores, document_paths = self.response_validator.verify_accuracy(
                generated_response, context_docs, validation_threshold
            )

            validated_sentences = [
                sentences[i] for i in range(len(sentences)) if similarity_scores[i] > validation_threshold
            ]
            validated_document_paths = [
                document_paths[i] for i in range(len(sentences)) if similarity_scores[i] > validation_threshold
            ]

            data["validated_sentences"] = validated_sentences
            data["validated_document_paths"] = validated_document_paths
            return data
        except Exception as e:
            raise PipelineExecutionError(
                stage=self.__class__.__name__, message=f"Response validation failed: {str(e)}"
            ) from e


class LLMQueryProcessingPipeline(Pipeline):
    """Orchestrates the sequence of stages for processing a user's prompt through the LLM pipeline.

    This pipeline defines a clear process flow:
      1. Fetching context documents.
      2. Enriching and formatting the prompt.
      3. Tokenizing the prompt for model consumption.
      4. Generating a response using the LLM.
      5. Decoding the model's tokenized output.
      6. Post-processing the decoded response.
      7. Validating the final response for accuracy and relevance.
    """

    def __init__(self):
        self.stages = [
            ContextDocumentFetcherStage(),  # Fetches relevant context documents.
            AugmentedPromptFormatterStage(),  # Formats prompt with contextual documents.
            ModelInputTokenizerStage(),  # Tokenizes the enriched prompt.
            LLMResponseGeneratorStage(),  # Generates response via LLM.
            ResponseDecoderStage(),  # Decodes tokenized output.
            ResponsePostProcessorStage(),  # Post-processes decoded response.
            ResponseAccuracyValidatorStage(),  # Validates response accuracy.
        ]
        super().__init__(self.stages)
