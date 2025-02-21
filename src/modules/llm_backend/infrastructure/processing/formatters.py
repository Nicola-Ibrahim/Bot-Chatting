from abc import ABC, abstractmethod

from .typedefs import Tokenizer


class ModelInputFormatter(ABC):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    @abstractmethod
    def format(self, user_query: str, context: str) -> str:
        pass


class ConversationalModelInputFormatter(ModelInputFormatter):
    @abstractmethod
    def format(self, user_query: str, context: str, chat_history: list[dict[str, str]]) -> str:
        pass


class LlamaFormatter(ConversationalModelInputFormatter):
    def format(self, user_query: str, context: str, chat_history: list[dict[str, str]]) -> str:
        system_message = (
            "This is a chat between a user and an artificial intelligence assistant. "
            "The assistant gives helpful, detailed, and polite answers to the user’s questions "
            "based on the provided context. The assistant must follow these rules:\n"
            "1. **Include Images**: If the context contains images, the assistant must include them in the response. "
            "The assistant must strictly extract and include any complete image directory paths exactly as they appear in the context, without modification.\n"
            "2. **Image Formatting**: The assistant must format images as HTML `<img>` tags. For example: `<img src='/path/to/image.png' alt='Image' style='max-width: 100%; height: auto;'>`.\n"
            "3. **No Hallucination**: The assistant does not invent or hallucinate image paths. If an image is not in the context, the assistant should not include it.\n"
            "4. **Complete Answers**: The assistant must provide full and complete answers to the user’s questions, including all relevant information from the context.\n"
            "5. **Indicate Missing Information**: If the context does not contain enough information to answer the question, the assistant should indicate this clearly."
        )

        instruction = (
            "Please give a full and complete answer for the question and include image paths from the context. "
            "The assistant must strictly extract and include any complete image directory paths exactly as they appear in the context, without modification. "
            "If the context contains images, the assistant must include them in the response as HTML `<img>` tags. "
            "For example: `<img src='/path/to/image.png' alt='Image' style='max-width: 100%; height: auto;'>`. "
            "If the context does not contain enough information to answer the question, please indicate this clearly."
            "Please give a full and complete answer for the question and include image paths and video paths from the context."
            "Please always provide mathematical expressions and formulas in the correct Latex format using Latex equations."
            "Please always format variable names as inline LaTeX using the $...$ notation. For example, write $x$ instead of x. "
        )

        context_text = context + "\n\n" if context else ""
        conversation = "\n\n".join(f"User: {c['question']}\n\nAssistant: {c['answer']}" for c in chat_history)

        if chat_history:
            chat_history[0]["question"] = instruction + chat_history[0]["question"]
            conversation += f"\n\nUser: {user_query}\n\nAssistant:"
        else:
            user_query = instruction + user_query
            conversation = f"User: {user_query}\n\nAssistant:"

        return f"{system_message}\n\n{context_text}{conversation}"


class QwenModelInputFormatter(ModelInputFormatter):
    def format(self, user_query: str, context: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "This is a chat between a user and an artificial intelligence assistant working for Optano. "
                "The assistant gives helpful, detailed, and polite answers to the user’s questions "
                "based on the context. The assistant should also indicate when the answer cannot be "
                "found in the context. In this case, the assistant answers with 'I cannot help you answering this question based on the documentation.'. It gives a full and complete answer for the question and include image paths from the context."
                "The assistant answers with the correct Latex Code using $...$ for short formulas and $$...$$ for longer formulas.",
            },
            {"role": "system", "content": context},
            {"role": "user", "content": user_query},
        ]
        return self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
