from ai.infra.pipe.base import Pipeline
from models.model_wrappers import LlmModel
from models.tokenizer_wrappers import LlmTokenizer
from common.infra.config import EXTERNAL_DATA_DIR, PROCESSED_DATA_DIR

from .generator import AnswerGenerator
from .preprocessor import Preprocessor
from .stage import AnswerGenerationStage, AnswerValidationStage, DocumentRetrievalStage

# Pre-process the external data once, used for answering questions
# This step is not repeated for every question to optimize performance
status = Preprocessor().preprocess(
    from_directory=EXTERNAL_DATA_DIR / 'optano', to_directory=PROCESSED_DATA_DIR / 'preprocessed_data'
)


# TODO: convert this to class
def generate_answer_for_prompt(message: str, streamer=None):
    """
    Generates an answer based on a user's input message by executing a multi-stage pipeline.

    The function uses a pipeline with the following stages:
      1. **DocumentRetrievalStage**: Retrieves relevant documents or information based on the input message.
      2. **AnswerGenerationStage**: Generates an answer from the retrieved documents.
      3. **AnswerValidationStage**: Validates the generated answer for accuracy and consistency.

    Args:
        message (str): A string representing the user's question or input message.

    Returns:
        tuple: A tuple containing:
            - answer (str): The generated answer based on the retrieved documents.
            - validated_sentences (list): A list of validated sentences that support the generated answer.

    Example:
        message = "What are the main features of seaborn library in Python?"
        answer, validated_sentences = generate_answer_from_question(message)
        # The function returns an answer and the validated sentences supporting the answer.
    """

    # Prepare the input data for the pipeline based on the user's message
    initial_data = {"message": message}

    # Create a shared instance of AnswerGenerator
    shared_answer_generator = AnswerGenerator(model=LlmModel(), tokenizer=LlmTokenizer())

    # Initialize the pipeline with the required stages for retrieving documents, generating an answer, and validating it
    pipeline = Pipeline(
        stages=[
            DocumentRetrievalStage(),  # First stage: Retrieve relevant documents or information
            AnswerGenerationStage(
                answer_generator=shared_answer_generator, streamer=streamer
            ),  # Second stage: Generate an answer from the retrieved information
            AnswerValidationStage(
                answer_generator=shared_answer_generator
            ),  # Third stage: Validate the answer for accuracy
        ]
    )

    # Run the pipeline and collect the results
    result = pipeline.run(initial_data)

    # Extract the generated answer and the validated supporting sentences
    answer = result["answer"]
    validated_sentences = result["validated_sentences"]
    validated_paths = result["validated_paths"]

    # Return the generated answer and validated supporting sentences
    return answer, validated_sentences, validated_paths
