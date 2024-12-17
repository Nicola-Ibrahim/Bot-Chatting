from typing import List, Tuple

from models.tokenizer_wrappers import Tokenizer


class AnswerValidator:
    """Class responsible for validating answers by comparing them with document content.

    This class uses a tokenizer to split sentences and employs TF-IDF and cosine similarity
    to assess the relevance of the answer in comparison to the sentences extracted from documents.

    Attributes:
        tokenizer (Tokenizer): The tokenizer used to split sentences from the answer and documents.
    """

    def __init__(self, tokenizer: Tokenizer) -> None:
        """Initializes the AnswerValidator with a tokenizer.

        Args:
            tokenizer (Tokenizer): The tokenizer used for splitting sentences.
        """
        self.tokenizer = tokenizer

    def execute(self, answer: str, documents: List[Tuple[str, str, int]]) -> Tuple[List[str], List[float], List[str]]:
        """Validates the generated answer by comparing it with the provided documents.

        This method splits the answer and document content into sentences, calculates TF-IDF
        representations, and measures the cosine similarity between them.

        Args:
            answer (str): The generated answer to validate.
            documents (List[Tuple[str, str, int]]): A list of tuples containing document metadata, content, and an integer.

        Returns:
            Tuple[List[str], List[float], List[str]]:
                - List[str]: The sentences extracted from the answer.
                - List[float]: The maximum similarity scores between the answer sentences and the document sentences.#
                - List[str]: Documents containing the maximum similarity scores
        """
        if answer is None or answer == "":
            return [""], [0]

        answer_sentences, answer_tokens = self.tokenizer.split_sentences(answer)
        document_tokens = self._extract_sentences_from_documents(documents)
        max_path, max_similarity = self._calculate_similarity(answer_tokens, document_tokens)
        return answer_sentences, max_similarity, max_path

    def _extract_sentences_from_documents(self, documents: List[Tuple[str, str, int]]) -> List[Tuple[str, List[str]]]:
        """Extracts and splits sentences from the provided document content.

        Args:
            documents (List[Tuple[str, str, int]]): A list of tuples containing document metadata, content, and an integer.

        Returns:
            List[Tuple[str, List[str]]]: A list of tuples containing the file path and a list of sentences extracted from the document content.
        """
        all_sentences = [(path, self.tokenizer.split_sentences(content)[1]) for path, content, _ in documents]
        return all_sentences

    def _calculate_similarity(self, answer_tokens, document_tokens) -> Tuple[List[str], List[float]]:
        """Calculates the cosine similarity between the answer and document sentences.

        Args:
            answer_tfidf: The TF-IDF matrix for the answer sentences.
            document_tfidf: The TF-IDF matrix for the document sentences.

        Returns:
            Tuple[List[str], List[float]]: A list of maximum similarity scores between each answer sentence and the
            document sentences together with the path containig the maximum score in another list.
        """

        max_similarity_per_sentence = []
        max_similarity_path_per_sentence = []

        for t in answer_tokens:
            max_path = ""
            max_sim = -float("inf")
            for path, documents in document_tokens:
                for doc_t in documents:
                    similarity = t.similarity(doc_t)
                    if similarity > max_sim:
                        max_path = path
                        max_sim = similarity
            max_similarity_per_sentence.append(max_sim)
            max_similarity_path_per_sentence.append(max_path)

        return max_similarity_path_per_sentence, max_similarity_per_sentence
