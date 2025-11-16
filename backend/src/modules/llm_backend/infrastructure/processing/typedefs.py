from typing import TypeVar

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser.text.sentence import SentenceSplitter
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer

LlmModel = TypeVar("LlmModel", bound=AutoModel | AutoModelForCausalLM)
EmbeddingModel = TypeVar("EmbeddingModel", bound=BaseEmbedding)
Tokenizer = TypeVar("Tokenizer", bound=AutoTokenizer)
SentenceSplitter = TypeVar("SentenceSplitter", bound=SentenceSplitter)
