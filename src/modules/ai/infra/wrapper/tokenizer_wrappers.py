from typing import List, Tuple
import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
import spacy


class Tokenizer:
    """Base class for different tokenizer implementations."""

    pass


class LlmTokenizer(Tokenizer):
    """Proxy class for interacting with the Llama model tokenizer from HuggingFace."""

    _instance = None

    def __new__(cls, model_name: str = None):
        """Ensures only one instance of the HuggingFace tokenizer is created."""
        if cls._instance is None:
            # Directly instantiate the HuggingFace tokenizer
            model_name = model_name or "nvidia/Llama3-ChatQA-2-8B"
            cls._instance = AutoTokenizer.from_pretrained(model_name)
        return cls._instance

    def __init__(self, model_name: str = None) -> None:
        """No need to initialize; handled in __new__."""
        pass

    def tokenize(self, text: str) -> List[int]:
        """Tokenizes the input text and returns a list of token IDs."""
        return self.encode(text)


class PunktTokenizer(Tokenizer):
    """Proxy class for sentence tokenization using NLTK's Punkt tokenizer."""

    _instance = None

    def __new__(cls):
        """Ensures only one instance of the Punkt tokenizer is created."""
        if cls._instance is None:
            # Initialize NLTK resources and return an instance of Punkt sentence tokenizer
            nltk.download("punkt")
            cls._instance = super(PunktTokenizer, cls).__new__(cls)
        return cls._instance

    def split_sentences(self, text: str) -> List[str]:
        """Splits the provided text into sentences using NLTK's sentence tokenizer."""
        sentences = sent_tokenize(text)
        sentences = [str.split(s, "\n") for s in sentences]  # Also split by line break (not done by Punkt)
        sentences = [s for sublist in sentences for s in sublist]  # Flatten list
        return self._filter_non_empty_sentences(sentences)

    def _filter_non_empty_sentences(self, sentences: List[str]) -> List[str]:
        """Filters out empty or whitespace-only sentences from the tokenized list."""
        return [sentence.strip() for sentence in sentences if sentence.strip()]


class SpaCyTokenizer(Tokenizer):
    """Proxy class for sentence tokenization using SpaCy tokenizer."""

    _instance = None
    _tokenizer = None

    def __new__(cls):
        """Ensures only one instance of the Punkt tokenizer is created."""
        if cls._instance is None:
            # Directly instantiate the HuggingFace tokenizer
            cls._tokenizer = spacy.load("en_core_web_sm")
            cls._instance = super(SpaCyTokenizer, cls).__new__(cls)
        return cls._instance

    def split_sentences(self, text: str) -> Tuple[List[str], List[spacy.tokens.Span]]:
        """Splits the provided text into sentences using NLTK's sentence tokenizer."""
        doc = self._tokenizer(text)
        result = []
        resultText = []
        for sent in doc.sents:
            if sent.text.strip() != "":
                result.append(sent)
                resultText.append(sent.text.strip())
        return resultText, result

    def _filter_non_empty_sentences(self, sentences: List[str]) -> List[str]:
        """Filters out empty or whitespace-only sentences from the tokenized list."""
        return [sentence.strip() for sentence in sentences if sentence.strip()]
