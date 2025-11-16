from llama_index.core import QueryBundle, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever


class VectorSearchEngine:
    """Handles vector-based similarity search operations"""

    def __init__(self, index: VectorStoreIndex, top_k: int = 4):
        self._retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k)

    def find_similar(self, query: QueryBundle) -> list[tuple[str, str, float]]:
        """Find similar documents with scores"""
        return [
            (node.metadata.get("file_path", "Unknown"), node.text, result.score)
            for result in self._retriever.retrieve(query)
            for node in [result.node]
        ]
