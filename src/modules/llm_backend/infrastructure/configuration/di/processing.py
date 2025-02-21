from dependency_injector import containers, providers
from llama_index.core.node_parser.text.sentence import SentenceSplitter

# from ...processing.formatters import QwenModelInputFormatter


class ProcessingDIContainer(containers.DeclarativeContainer):
    """Container for text processing components"""

    tokenizer = providers.Dependency()

    # Sentence splitting
    sentence_splitter = providers.Resource(SentenceSplitter, paragraph_separator="\n\n\n", chunk_size=512)
