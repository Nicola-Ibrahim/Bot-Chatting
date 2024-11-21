import uuid

from chat.domain.entities.conversation import Conversation
from chat.domain.entities.message import Message
from src.shared.domain.exception import InValidOperationException
from src.shared.domain.result import Result

from ..interfaces.ai_services import AbstractResponseGeneratorService
from ..interfaces.conversation_repository import AbstractConversationRepository


class ConversationApplicationService:
    """
    Orchestrator for managing conversation-related operations. This class handles messages
    between domain models, domain services, and infrastructure services. It provides
    a high-level interface for starting, updating, retrieving, and managing conversations
    while delegating domain logic to specific domain entities and services.
    """

    def __init__(
        self,
        conversation_downloader: ConversationDownloader,
        repository: AbstractConversationRepository,
        response_generator: AbstractResponseGeneratorService,
        tokenizer: AbstractTokenizerService,
    ):
        """
        Initializes the gateway with necessary services and repositories.

        Args:
            conversation_downloader (ConversationDownloader): Service for downloading conversation data.
            repository (AbstractConversationRepository): Repository for storing and retrieving conversations.
            response_generator (AbstractResponseGeneratorService): Service for generating responses.
            tokenizer (AbstractTokenizerService): Tokenizer for managing token-related constraints.
        """
        self._conversation_downloader = conversation_downloader
        self._repository = repository
        self._response_generator = response_generator
        self._tokenizer = tokenizer

    def create_conversation(self) -> Result:
        """
        Creates a new conversation session and stores it in the repository.

        Returns:
            Result: A Result containing either the created Conversation or an error.
        """
        result = Conversation.create()

        # Save the conversation to the repository
        self._repository.save(result.value)

        return result

    def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Result:
        """
        Retrieves a conversation by its unique identifier.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.

        Returns:
            Result: A Result containing the retrieved Conversation or an error.
        """
        conversation = self._repository.get_by_id(conversation_id)

        result = Conversation.from_existing(conversation=conversation)

        return result

    def add_message(self, conversation_id: uuid.UUID, text: str) -> Result:
        """
        Adds a new message to a specific conversation and generates a response.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            text (str): The text of the new message.

        Returns:
            Result: A Result containing the created message or an error.
        """

        conversation = self._repository.get_by_id(conversation_id)

        conversation: Conversation = Conversation.from_existing(conversation=conversation)

        response = self._response_generator.generate_answer(text)

        # Add the message and generate the response
        result = conversation.add_message(text=text, response=response)

        self._repository.save(conversation=conversation)

        return result

    def regenerate_or_edit_message(self, conversation_id: uuid.UUID, message_id: uuid.UUID, text: str) -> Result:
        """
        Regenerates the response for a specific message in a conversation.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            message_id (uuid.UUID): The unique ID of the message.
            text (str): The new message text for the response generation.

        Returns:
            Result: A Result containing the regenerated response or an error.
        """
        conversation_result = self.get_conversation_by_id(conversation_id)
        if conversation_result.is_error:
            return conversation_result

        conversation = conversation_result.value
        new_response = self._response_generator.generate(text)

        # Edit or regenerate the message
        conversation.regenerate_or_edit_message(message_id=message_id, text=text, response=new_response)
        self._repository.save(conversation)

        return Result.success(new_response)

    def delete_conversation(self, conversation_id: uuid.UUID) -> Result:
        """
        Deletes a conversation session from the repository.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation to delete.

        Returns:
            Result: A Result indicating the outcome of the delete operation.
        """
        conversation_result = self.get_conversation_by_id(conversation_id)
        if conversation_result.is_error:
            return conversation_result

        self._repository.delete(conversation_id)
        return Result.success(None)

    def download_conversation(self, conversation_id: uuid.UUID) -> Result:
        """
        Downloads the content of a conversation using the specified download service.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation to download.

        Returns:
            Result: A Result indicating the outcome of the download operation.
        """
        conversation_result = self.get_conversation_by_id(conversation_id)
        if conversation_result.is_error:
            return conversation_result

        conversation = conversation_result.value
        self._conversation_downloader.download_conversation(conversation)
        return Result.success(None)

    def get_recent_messages(self, conversation_id: uuid.UUID, max_recent: int = 5, token_limit: int = 500) -> Result:
        """
        Retrieves recent messages from a conversation, respecting a token limit.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            max_recent (int, optional): The maximum number of recent messages to retrieve. Defaults to 5.
            token_limit (int, optional): The maximum token limit for the context. Defaults to 500.

        Returns:
            Result: A Result containing a list of messages or an error.
        """
        conversation_result = self.get_conversation_by_id(conversation_id)
        if conversation_result.is_error:
            return conversation_result

        conversation = conversation_result.value
        recent_messages = conversation.get_recent_messages(max_recent=max_recent, token_limit=token_limit)
        return Result.success(recent_messages)

    def read_plain_message_responses(
        self, conversation_id: uuid.UUID, max_recent: int = 5, token_limit: int = 500
    ) -> Result:
        """
        Retrieves the most recent plain message responses from a conversation.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            max_recent (int, optional): The maximum number of recent messages to retrieve. Defaults to 5.
            token_limit (int, optional): The maximum token limit for the context. Defaults to 500.

        Returns:
            Result: A Result containing a list of message responses or an error.
        """
        conversation_result = self.get_conversation_by_id(conversation_id)
        if conversation_result.is_error:
            return conversation_result

        conversation = conversation_result.value
        last_messages = conversation.get_last_n_messages(max_recent)

        selected_messages = []
        total_tokens = 0

        for message in reversed(last_messages):
            prompt_tokens = self._tokenizer.tokenize(message.text)
            response_tokens = self._tokenizer.tokenize(message.response.text if message.response else "")
            total = len(prompt_tokens) + len(response_tokens)

            if total_tokens + total > token_limit:
                break

            selected_messages.insert(0, message)
            total_tokens += total

        return Result.success(selected_messages)
