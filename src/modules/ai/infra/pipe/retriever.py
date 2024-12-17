from typing import List, Tuple

from llama_index.core import QueryBundle, Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

from models.model_wrappers import BaseModel


class DocumentRetriever:
    """Class responsible for searching documents based on a message.

    This class handles the initialization of document retrieval using an embedding model
    and an optional language model. It builds an index from documents and queries it
    to find relevant documents based on a provided message.

    Attributes:
        directory_path (str): The path to the directory containing the documents.
        embedding_model (BaseModel): The embedding model used for document retrieval.
        language_model (BaseModel, optional): The language model used for response generation.
    """

    def __init__(self, directory_path: str, embedding_model: BaseModel, language_model: BaseModel = None) -> None:
        """Initializes the DocumentRetriever with a directory path, embedding model, and optional language model.

        Args:
            directory_path (str): The path to the directory containing the documents.
            embedding_model (BaseModel): The embedding model for document retrieval.
            language_model (BaseModel, optional): The language model for response generation. Defaults to None.
        """
        self.directory_path = directory_path
        self.embedding_model = embedding_model
        self.language_model = language_model

        # Set the embed model and LLM (optional) in Settings
        Settings.embed_model = self.embedding_model
        if self.language_model:
            Settings.llm = self.language_model

    def execute(self, message: str) -> List[Tuple[str, str, float]]:
        """Searches for documents related to the provided message using the embedding model.

        Args:
            message (str): The message or question to search documents for.

        Returns:
            List[Tuple[str, str, float]]: A list of tuples where each tuple contains the file name, response text, and score.
        """
        index = self.build_document_index()
        query_bundle = QueryBundle(message)
        return self.query_index_with_file_path(index, query_bundle)

    def build_document_index(self) -> VectorStoreIndex:
        """Builds an index from documents in the specified directory using the embedding model.

        Returns:
            VectorStoreIndex: The created index from the documents.
        """
        # Load the documents from the specified directory
        documents = SimpleDirectoryReader(self.directory_path, recursive=True).load_data()

        # Use the embedding model from the BaseModel instance to create an index
        return VectorStoreIndex.from_documents(documents)

    def query_index_with_file_name(
        self, index: VectorStoreIndex, query_bundle: QueryBundle
    ) -> List[Tuple[str, str, float]]:
        """Queries the index and retrieves file names along with responses.

        Args:
            index (VectorStoreIndex): The index to query.
            query_bundle (QueryBundle): The query bundle containing the message.

        Returns:
            List[Tuple[str, str, float]]: A list of tuples where each tuple contains the file name, response text, and score.
        """
        # Use the embedding model from the BaseModel instance to retrieve documents
        retriever = VectorIndexRetriever(index=index, similarity_top_k=4)

        responses = [
            (node.metadata.get("file_name", "Unknown"), node.text, node_with_score.score)
            for node_with_score in retriever.retrieve(query_bundle)
            for node in [node_with_score.node]
        ]
        # print(responses[0])
        return responses

    def query_index_with_file_path(
        self, index: VectorStoreIndex, query_bundle: QueryBundle
    ) -> List[Tuple[str, str, float]]:
        """Queries the index and retrieves file names along with responses.

        Args:
            index (VectorStoreIndex): The index to query.
            query_bundle (QueryBundle): The query bundle containing the message.

        Returns:
            List[Tuple[str, str, float]]: A list of tuples where each tuple contains the file name, response text, and score.
        """
        # Use the embedding model from the BaseModel instance to retrieve documents
        retriever = VectorIndexRetriever(index=index, similarity_top_k=4)

        responses = [
            (node.metadata.get("file_path", "Unknown"), node.text, node_with_score.score)
            for node_with_score in retriever.retrieve(query_bundle)
            for node in [node_with_score.node]
        ]
        # print(responses[0])
        return responses
