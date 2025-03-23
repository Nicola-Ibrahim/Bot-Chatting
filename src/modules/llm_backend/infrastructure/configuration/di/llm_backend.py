from dependency_injector import containers, providers

from .models import ModelsDIContainer
from .processing import ProcessingDIContainer
from .search import SearchDIContainer


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
