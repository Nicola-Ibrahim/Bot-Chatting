from dependency_injector import containers, providers

from ...processing.loaders import ModelLoader, TokenizerLoader
from ...processing.streamers import ChunkedTextStreamer


class ModelsDIContainer(containers.DeclarativeContainer):
    """Container for model-related components"""

    config = providers.Configuration()

    embedding_model = providers.Resource(ModelLoader.load_embedding_model, config.embedding_model_name)

    llm_model = providers.Resource(ModelLoader.load_llm_model, config.llm_model_name)

    tokenizer = providers.Resource(TokenizerLoader.load_tokenizer, config.llm_tokenizer_name)

    text_streamer = providers.Factory(ChunkedTextStreamer, tokenizer=tokenizer, skip_prompt=config.skip_prompt)
