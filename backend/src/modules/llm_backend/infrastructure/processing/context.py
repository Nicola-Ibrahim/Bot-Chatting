from typing import Optional

from dependency_injector.wiring import Provide, inject
from llama_index.core import QueryBundle

from src.llm_backend.infrastructure.processing.search_engines import VectorSearchEngine

from ..configuration.di.containers import LLMBackendContainer


class DocumentFetcher:
    """Coordinates document retrieval workflow with enhanced error handling"""

    @inject
    def __init__(
        self,
        search_engine: VectorSearchEngine = Provide[LLMBackendContainer.search.search_engine],
        # text_processor: TextProcessor = None,
    ):
        self.search_engine = search_engine
        # self.text_processor = text_processor
        self._query_count = 0  # Simple usage metric

    def retrieve_documents(self, query: str, context_id: Optional[str] = None) -> list:
        """Execute full retrieval pipeline with error handling"""
        self._query_count += 1

        try:
            # Step 1: Query enhancement
            # processed_query = self.text_processor.format_query(query, context_id)

            # Step 2: Convert to query bundle
            query_bundle = QueryBundle(query)

            # Step 3: Execute search
            raw_results = self.search_engine.find_similar(query_bundle)

            # Step 4: Normalize results
            return raw_results

        except Exception as e:
            return []
