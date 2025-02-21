import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from dependency_injector.wiring import Provide, inject
from llama_index.core import QueryBundle

from src.llm_backend.infrastructure.configuration.di.llm_backend import LLMBackendContainer
from src.llm_backend.infrastructure.processing.search_engines import VectorSearchEngine
from src.llm_backend.infrastructure.processing.typedefs import Tokenizer
from src.paths import MEMORY_DIR

from ...infrastructure.configuration.di.llm_backend import LLMBackendContainer


class MemoryManager:
    """Manages memory for previous conversations, allowing the chatbot to retain context."""

    @inject
    def __init__(
        self,
        tokenizer: Tokenizer = Provide[LLMBackendContainer.models.tokenizer],
        memory_file: str = "chat_memory.json",
        token_limit: int = 500,
        max_recent: int = 5,
    ):
        self.memory_file = os.path.join(MEMORY_DIR, memory_file)
        self.token_limit = token_limit
        self.max_recent = max_recent
        self.tokenizer = tokenizer

        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as file:
                json.dump([], file)

    def _calculate_tokens(self, text: str) -> int:
        """Calculate the number of tokens in a given text."""
        return len(self.tokenizer.tokenize(text))

    def add_memory(self, question: str, answer: str):
        """Add a question-answer pair to memory."""
        with open(self.memory_file, "r+") as file:
            try:
                memories = json.load(file)
            except json.JSONDecodeError:
                memories = []
            memories.append({"id": len(memories), "question": question, "answer": answer})
            file.seek(0)
            json.dump(memories, file, indent=4)
            file.truncate()
        return len(memories) - 1  # Return prompt ID

    def get_recent_memory(self, prompt_id=None) -> List[Dict[str, str]]:
        """Retrieve up to max_recent memories, limited by a total token count. If a prompt is provided, only memories before the prompt are returned. The prompts after are deleted"""
        with open(self.memory_file, "r") as file:
            try:
                memories = json.load(file)
            except json.JSONDecodeError:
                return []

        if prompt_id:  # Delete all memories after prompt ID if prompt_id is provided
            index = [i for i, memory in enumerate(memories) if memory["id"] == int(prompt_id)]
            if len(index) == 1:
                index = index[0]
                memories = memories[:index]
                with open(self.memory_file, "r+") as f:
                    f.seek(0)
                    json.dump(memories, f, indent=4)
                    f.truncate()

        recent_memories = memories[-self.max_recent :]
        filtered_memories = []
        total_tokens = 0
        used_memory_count = 0

        for memory in reversed(recent_memories):
            tokens = self._calculate_tokens(memory["question"]) + self._calculate_tokens(memory["answer"])
            if total_tokens + tokens > self.token_limit:
                break
            filtered_memories.insert(0, memory)
            total_tokens += tokens
            used_memory_count += 1

        return filtered_memories

    def get_all_memory(self):
        """Retrieve the full conversation history."""
        with open(self.memory_file, "r") as file:
            try:
                memories = json.load(file)
            except json.JSONDecodeError:
                memories = []
            return memories if memories else []

    def clear_memory(self):
        """Clears all stored memories."""
        with open(self.memory_file, "w") as f:
            json.dump([], f)

    def remove_memory(self, memory_id) -> None:
        """Removes a memory by its ID."""
        with open(self.memory_file, "r+") as f:
            memories = json.load(f)
            memories = [memory for memory in memories if memory["id"] != memory_id]
            f.seek(0)
            json.dump(memories, f, indent=4)
            f.truncate()


class TextProcessor:
    """Handles all text processing and formatting operations"""

    @inject
    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    def format_query(self, raw_query: str, context_id: Optional[str] = None) -> str:
        """Enhances queries with contextual memory"""
        try:
            # Base query formatting
            formatted = raw_query.strip()

            # Add conversation context if available
            if context_id:
                memories = self.memory_manager.get_recent_memory(context_id)
                if memories:
                    context = "\n".join(f"Q: {m['question']}\nA: {m['answer']}" for m in memories)
                    formatted = f"Context:\n{context}\n\nNew Question: {formatted}"

            return formatted

        except Exception as e:
            return raw_query  # Fallback to raw input


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
