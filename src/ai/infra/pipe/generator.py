import re
from typing import Any, Dict, List, Tuple

from models.model_wrappers import BaseModel
from models.tokenizer_wrappers import Tokenizer

from .memory import MemoryManager


class AnswerGenerator:
    """Generates answers based on a model, tokenizer, and provided documents.

    This class uses a language model and tokenizer to generate answers based on
    documents and a message provided by the user. It prepares the documents,
    formats the input, and generates a response from the model.

    Attributes:
        llm (BaseModel): An instance of a model implementing the BaseModel interface.
        tokenizer (Tokenizer): An instance of a tokenizer for processing input.
    """

    def __init__(self, model: BaseModel, tokenizer: Tokenizer) -> None:
        """Initializes the AnswerGenerator with a model and tokenizer.

        Args:
            model (BaseModel): An instance of a model implementing the BaseModel interface.
            tokenizer (Tokenizer): An instance of a tokenizer for processing input.
        """
        self.llm_model = model
        self.tokenizer = tokenizer
        self.memory_manager = MemoryManager()

    def execute(
        self,
        files: List[Tuple[str, str, Any]],
        message: str,
        doc_count: int = 2,
        temperature: float = 1.0,
        streamer=None,
    ) -> str:
        """Generates an answer based on the provided documents and message.

        Args:
            files (List[Tuple[str, str, Any]]): A list of tuples where each tuple contains
                metadata, content, and any additional information about a document.
            message (str): The question or message for which the answer is generated.
            doc_count (int, optional): The number of documents to include in the context.
                Defaults to 2.

        Returns:
            str: The generated answer as a string.
        """
        context = self._prepare_documents(files, doc_count)
        answer = self.generate(message, context, temperature, streamer)
        return answer

    def _get_recent_memories(self) -> str:
        """Formats recent memory for inclusion in the context."""
        memories = self.memory_manager.get_recent_memory()
        return " ".join(f"Q: {mem['question']} A: {mem['answer']}" for mem in memories)

    def _prepare_documents(self, files: List[Tuple[str, str, Any]], doc_count: int) -> str:
        """Prepares and concatenates the content of the extracted documents.

        Args:
            files (List[Tuple[str, str, Any]]): A list of tuples containing document metadata
                and content.
            doc_count (int): The number of documents to include in the context.

        Returns:
            str: The concatenated content of the selected documents.
        """
        selected_files = files[:doc_count] if doc_count > 0 else files
        return " ".join(content for _, content, _ in selected_files)

    def generate(self, message: str, context: str, temperature: float = 1.0, streamer=None) -> str:
        """Generates a response from the model based on the given message and context.

        Args:
            message (str): The question or message for which the response is generated.
            context (str): The context extracted from the documents to help generate the response.

        Returns:
            str: The generated response as a string.
        """
        memory_manager = MemoryManager()
        recent_memories = memory_manager.get_recent_memory()
        formatted_input = self._format_input(message, context, recent_memories)
        # print(formatted_input)
        tokenized_prompt = self.tokenizer(self.tokenizer.bos_token + formatted_input, return_tensors="pt").to(
            self.llm_model.device
        )

        # Set the token termination criteria
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        if streamer is not None:
            streamer.tokenizer = self.tokenizer

        outputs = self.llm_model.generate(
            input_ids=tokenized_prompt.input_ids,
            attention_mask=tokenized_prompt.attention_mask,
            max_new_tokens=512,
            temperature=0.6,
            do_sample=True,
            eos_token_id=terminators,
            streamer=streamer,
        )
        response = outputs[0][tokenized_prompt.input_ids.shape[-1] :]

        return self.tokenizer.decode(response, skip_special_tokens=True)

    def _format_input(self, message: str, context: str, previous_chat: List[Dict[str, str]]) -> str:
        """Formats the input for the model based on the message and context.

        Args:
            message (str): The question or message provided by the user.
            context (str): The context extracted from the documents.

        Returns:
            str: The formatted input string combining system message, context, and message.
        """
        system_message = (
            "This is a chat between a user and an AI assistant, that helps in questions about the usage of Optano. "
            "The assistant provides helpful, complete, detailed, and polite answers to the user's last message using the given context. "
            "The assistant gets information from the given context. "
            "The assistant always includes the images and icons from the context. "
            "When the assistant recognizes an image or icon within the context, it generates the complete path of it. "
            "The assistant must strictly extract and include complete image or icon directory paths exactly as they appear in the context, without modification. "
            "The assistant does not hallucinate and does not invent image paths. "
        )

        context = "Context: " + context

        images = "Images: " + "\n".join(re.findall(r"(/static[^\.]*\.(?:png|jpg))", context))

        memory_context = "\n".join(f"User: {c['question']}\n Assistant: {c['answer']}" for c in previous_chat)

        conversation = f"User: {message}\nAssistant:"

        # instruction = " Provide a complete and detailed response to the user's query and specifically use the relevant image paths or links mentioned in the context to support each step in your response. For example, when you mention a step or an icon, clearly associate it with the corresponding image path from the context."
        print(f"{system_message}\n\n{context}\n\n{images}\n\n{memory_context}\n{conversation}")
        return f"{system_message}\n\n{context}\n\n{images}\n\n{memory_context}\n{conversation}"
