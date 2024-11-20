from ..entities.conversation import Conversation
from ..entities.message import Content


class MessageDomainService:
    @staticmethod
    def read_chat_partially(
        chat: Chat, tokenizer: AbstractTokenizerService, max_recent: int = 5, token_limit: int = 500
    ) -> list[Content]:
        """
        Retrieve recent messages from a chat, respecting a token limit.

        Args:
            chat_id (uuid.UUID): The ID of the chat.
            max_recent (int): The maximum number of recent messages to retrieve.
            token_limit (int): The maximum token limit for the context.

        Returns:
            list[Content]: A list of recent messages within the token limit.

        Raises:
            BusinessValidationException: If the chat does not exist.
        """

        # Retrieve recent messages
        last_messages = chat.get_last_n_messages(max_recent)

        selected_messages = []
        total_tokens = 0

        for message in reversed(last_messages):
            prompt_tokens = tokenizer.tokenize(message.text)
            response_tokens = tokenizer.tokenize(message.response.text if message.response else "")
            total = len(prompt_tokens) + len(response_tokens)

            if total_tokens + total > token_limit:
                break

            selected_messages.insert(0, message)
            total_tokens += total

        return selected_messages
