from dependency_injector import containers, providers
from llama_index.core.node_parser.text.sentence import SentenceSplitter

from ...processing.indexers import IndexBuilder
from ...processing.loaders import ModelLoader, TokenizerLoader
from ...processing.search_engines import VectorSearchEngine
from ...processing.streamers import ChunkedTextStreamer


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


class ProcessingDIContainer(containers.DeclarativeContainer):
    """Container for text processing components"""

    tokenizer = providers.Dependency()

    # Sentence splitting
    sentence_splitter = providers.Factory(SentenceSplitter, paragraph_separator="\n\n\n", chunk_size=512)


class ModelsDIContainer(containers.DeclarativeContainer):
    """Container for model-related components"""

    config = providers.Configuration()

    embedding_model = providers.Resource(ModelLoader.load_embedding_model, config.embedding_model_name)

    llm_model = providers.Resource(ModelLoader.load_llm_model, config.llm_model_name)

    tokenizer = providers.Resource(TokenizerLoader.load_tokenizer, config.llm_tokenizer_name)

    text_streamer = providers.Factory(ChunkedTextStreamer, tokenizer=tokenizer, skip_prompt=config.skip_prompt)


class LLMBackendContainer(containers.DeclarativeContainer):
    """Root application container"""

    config = providers.Configuration()

    # Wiring configuration
    wiring_config = containers.WiringConfiguration(
        modules=["src.web.chat.endpoints"],
        packages=["src.llm_backend.application.prompt", "src.llm_backend.application.excel", "src.tests"],
    )

    # Sub-containers
    models = providers.Container(ModelsDIContainer, config=config.models)

    processing = providers.Container(ProcessingDIContainer, tokenizer=models.tokenizer.provided)

    search = providers.Container(
        SearchDIContainer,
        config=config.search,
        embedding_model=models.embedding_model.provided,
        sentence_splitter=processing.sentence_splitter.provided,
    )
