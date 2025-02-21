from typing import List, Tuple

from bs4 import BeautifulSoup
from dependency_injector.wiring import Provide, inject
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser.text.sentence import SentenceSplitter

from ...infrastructure.configuration.di.llm_backend import LLMBackendContainer


class ResponseValidator:
    """Class responsible for validating answers."""

    @inject
    def __init__(
        self,
        embedding_model: BaseEmbedding = Provide[LLMBackendContainer.models.embedding_model],
        sentence_splitter: SentenceSplitter = Provide[LLMBackendContainer.processing.sentence_splitter],
    ) -> None:
        """Initializes the ResponseValidator."""
        self.embedding_model = embedding_model
        self.sentence_splitter = sentence_splitter

    def verify_accuracy(
        self, answer: str, documents: List[Tuple[str, str, int]], validation: float = 0.85
    ) -> Tuple[List[str], List[float], List[str]]:
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
                - List[str]: Document path containing the maximum similarity scores
        """
        if answer is None or answer == "":
            return [""], [0]

        answer = BeautifulSoup(markup=answer, features="html.parser").get_text()

        answer_sentences = self._split_sentences(answer)
        answer_sentences = [s for s in answer_sentences if len(s.strip()) > 0]  # Remove empty sentences
        document_sentences = self._extract_sentences_from_documents(documents[:1])
        max_path, max_similarity = self._calculate_similarity(answer_sentences, document_sentences, validation)
        return answer_sentences, max_similarity, max_path

    def _split_sentences(self, text: str) -> List[str]:
        """Splits the provided text into sentences.

        Args:
            text (str): The text to split into sentences.

        Returns:
            List[str]: A list of sentences extracted from the text.
        """
        splits = [text]
        for split_fn in self.sentence_splitter._split_fns:
            temp_splits = []
            for s in splits:
                split = split_fn(s)
                if len(split) > 1:
                    temp_splits.extend(split)
                else:
                    temp_splits.append(s)
            splits = temp_splits

        return splits

    def _extract_sentences_from_documents(self, documents: List[Tuple[str, str, int]]) -> List[Tuple[str, List[str]]]:
        """Extracts and splits sentences from the provided document content.

        Args:
            documents (List[Tuple[str, str, int]]): A list of tuples containing document metadata, content, and an integer.

        Returns:
            List[Tuple[str, List[str]]]: A list of tuples containing the file path and a list of sentences extracted from the document content.
        """
        all_sentences = [(path, self._split_sentences(content)) for path, content, _ in documents]
        return all_sentences

    def _calculate_similarity(self, answer_sentences, document_sentences, validation) -> Tuple[List[str], List[float]]:
        """Calculates the cosine similarity between the answer and document sentences.

        Args:
            answer_sentences: The TF-IDF matrix for the answer sentences.
            document_sentences: The TF-IDF matrix for the document sentences.

        Returns:
            Tuple[List[str], List[float]]: A list of maximum similarity scores between each answer sentence and the
            document sentences together with the path containig the maximum score in another list.
        """

        max_similarity_per_sentence = []
        max_similarity_path_per_sentence = []

        for t in answer_sentences:
            max_path = ""
            max_sim = -float("inf")
            emb1 = self.embedding_model.get_text_embedding(t)
            for path, documents in document_sentences:
                for doc_t in documents:
                    emb2 = self.embedding_model.get_text_embedding(doc_t)
                    similarity = self.embedding_model.similarity(emb1, emb2)
                    if similarity > max_sim:
                        max_path = path
                        max_sim = similarity
                    if max_sim > validation:
                        break
            max_similarity_per_sentence.append(max_sim)
            max_similarity_path_per_sentence.append(max_path)

        return max_similarity_path_per_sentence, max_similarity_per_sentence
