from ...application import AbstractResponseGenerator
from .pipe.runner import generate_answer_for_prompt


class ResponseGenerator(AbstractResponseGenerator):
    def generate_answer(self, prompt_text: str) -> str:
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

        answer, validated_sentences, validated_paths = generate_answer_for_prompt(message=prompt_text)
        return answer, validated_sentences, validated_paths
