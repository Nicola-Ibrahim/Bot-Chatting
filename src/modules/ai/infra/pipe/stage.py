from typing import Any, Dict, List

from ai.infra.pipe.base import PipelineStage
from models.model_wrappers import EmbeddingModel, HuggingFaceLargeLanguageModel, LlmModel
from models.tokenizer_wrappers import LlmTokenizer, PunktTokenizer, SpaCyTokenizer
from common.infra.config import PROCESSED_DATA_DIR
from src.chats.infra.logging.loggers import FileLogger

from .generator import AnswerGenerator
from .retriever import DocumentRetriever
from .validator import AnswerValidator

logger = FileLogger(__name__, "prompt_pipeline_stage")


class DocumentRetrievalStage(PipelineStage):
    """Pipeline stage responsible for retrieving documents based on a message."""

    def __init__(self) -> None:
        """Initializes the DocumentRetrievalStage."""
        # Initialize the logger for this stage
        logger.info("Initializing DocumentRetrievalStage")

        self.document_retriever = DocumentRetriever(
            directory_path=PROCESSED_DATA_DIR / "preprocessed_data",
            embedding_model=EmbeddingModel(),
            language_model=HuggingFaceLargeLanguageModel(),
        )

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieves documents based on the message provided in the data."""
        message = data["message"]
        logger.debug(f"Received message for document retrieval: {message}")
        documents = self.document_retriever.execute(message)
        logger.info(f"Retrieved {len(documents)} documents")
        return {"documents": documents}


class AnswerGenerationStage(PipelineStage):
    """Pipeline stage responsible for generating an answer based on retrieved documents."""

    def __init__(self, answer_generator: AnswerGenerator = None, streamer=None) -> None:
        """Initializes the AnswerGenerationStage."""
        # Initialize the logger for this stage

        logger.info("Initializing AnswerGenerationStage")
        self.answer_generator = (
            answer_generator
            if answer_generator is not None
            else AnswerGenerator(model=LlmModel(), tokenizer=LlmTokenizer())
        )
        self.streamer = streamer

    def process(self, data: Dict[str, Any], temperature: float = 1.0) -> Dict[str, Any]:
        """Generates an answer based on the documents and message provided in the data."""
        documents: List[Dict[str, Any]] = data["documents"]
        message: str = data["message"]
        logger.debug(f"Generating answer with message: {message} and {len(documents)} documents")
        answer = self.answer_generator.execute(documents, message, temperature=temperature, streamer=self.streamer)
        logger.info("Generated answer successfully")
        return {"answer": answer}


class AnswerValidationStage(PipelineStage):
    """Pipeline stage responsible for validating the generated answer."""

    def __init__(self, answer_validator: AnswerValidator = None, answer_generator: AnswerGenerator = None) -> None:
        """Initializes the AnswerValidationStage."""

        logger.info("Initializing AnswerValidationStage")
        self.answer_generator = (
            answer_generator
            if answer_generator is not None
            else AnswerGenerator(model=LlmModel(), tokenizer=LlmTokenizer())
        )
        self.answer_validator = (
            answer_validator if answer_validator is not None else AnswerValidator(tokenizer=SpaCyTokenizer())
        )
        self.max_retries = 0
        self.initial_temperature = 0.1
        self.min_temperature = 0.1

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validates the generated answer based on the documents provided in the data."""
        answer: str = data["answer"]
        documents: List[Dict[str, Any]] = data["documents"]
        temperature = self.initial_temperature
        retries = 0
        answer_generation_stage = AnswerGenerationStage(self.answer_generator)

        logger.debug(f"Validating answer: {answer} against {len(documents)} documents")

        sentences, similarity, paths = self.answer_validator.execute(answer, documents)

        # Check if any sentence passes the similarity threshold
        if any(sim >= 0.5 for sim in similarity):
            validated_sentences = [sentences[i] for i in range(len(sentences)) if similarity[i] > 0.5]
            validated_sentences_paths = [paths[i] for i in range(len(sentences)) if similarity[i] > 0.5]
            logger.info(f"Validated and filtered {len(validated_sentences)} sentences with similarity > 0.5")
            return {
                "validated_sentences": validated_sentences,
                "answer": answer,
                "validated_paths": validated_sentences_paths,
            }

        while retries < self.max_retries and temperature >= self.min_temperature:
            # If validation fails, lower the temperature and try again
            logger.warning(
                f"Validation failed at temperature {temperature}. Lowering temperature and regenerating answer."
            )
            temperature /= 2  # Lower the temperature
            retries += 1

            # Regenerate the answer with a lower temperature
            generated_output = answer_generation_stage.process(data, temperature=temperature)
            answer = generated_output["answer"]
            logger.debug(f"Validating answer: {answer} against {len(documents)} documents")
            sentences, similarity, paths = self.answer_validator.execute(answer, documents)

            # Check if any sentence passes the similarity threshold
            if any(sim >= 0.5 for sim in similarity):
                validated_sentences = [sentences[i] for i in range(len(sentences)) if similarity[i] > 0.5]
                validated_sentences_paths = [paths[i] for i in range(len(sentences)) if similarity[i] > 0.5]
                logger.info(f"Validated and filtered {len(validated_sentences)} sentences with similarity > 0.5")
                return {
                    "validated_sentences": validated_sentences,
                    "answer": answer,
                    "validated_paths": validated_sentences_paths,
                }

        # If all retries fail, return the last attempted answer
        logger.error(f"Failed to validate the answer after {self.max_retries} retries.")
        return {
            "validated_sentences": [],
            "answer": answer,
            "validated_paths": [],
        }  # Return the last answer if validation continues to fail
