from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex

from .typedefs import EmbeddingModel, SentenceSplitter


class IndexBuilder:
    """Builds and manages the vector store index"""

    def __init__(self, data_dir: str, embedding_model: EmbeddingModel, sentence_splitter: SentenceSplitter):
        self.data_dir = data_dir
        Settings.embed_model = embedding_model
        Settings.text_splitter = sentence_splitter
        self.index = self._build_index()

    def _build_index(self) -> VectorStoreIndex:
        """Construct vector index from documents"""
        documents = SimpleDirectoryReader(input_dir=self.data_dir, recursive=True).load_data()
        return VectorStoreIndex.from_documents(documents, show_progress=True)
