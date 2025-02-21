from dependency_injector import containers, providers

from ...processing.indexers import IndexBuilder
from ...processing.search_engines import VectorSearchEngine


class SearchDIContainer(containers.DeclarativeContainer):
    """Container for search-related components"""

    config = providers.Configuration()

    embedding_model = providers.Dependency()
    sentence_splitter = providers.Dependency()

    # Index construction
    index_builder = providers.Resource(
        IndexBuilder,
        data_dir=config.processed_data_dir,
        embedding_model=embedding_model,
        sentence_splitter=sentence_splitter,
    )

    # Search engine
    search_engine = providers.Resource(VectorSearchEngine, index=index_builder.provided.index, top_k=config.top_k)
