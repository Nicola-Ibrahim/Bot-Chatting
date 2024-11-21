import uuid

from ...domain import MessageDomainService
from ...domain.entities.conversation import Conversation
from ...domain.entities.message import Message
from ..interfaces.ai_services import AbstractResponseGeneratorService, AbstractTokenizerService
from ..interfaces.conversation_repository import AbstractConversationRepository


class ConversationApplicationGateway:
    """
    Orchestrator for managing conversation-related operations. This class handles messages
    between domain models, domain services, and infrastructure services. It provides
    a high-level interface for starting, updating, retrieving, and managing conversations
    while delegating domain logic to specific domain entities and services.
    """

    def __init__(
        self,
        conversation_download_service: ConversationDownloadService,
        repository: AbstractConversationRepository,
        response_generator: AbstractResponseGeneratorService,
        tokenizer: AbstractTokenizerService,
        feedback_repo: AbstractFeedbackRepository,
    ):
        """
        Initializes the gateway with necessary services and repositories.

        Args:
            conversation_download_service (ConversationDownloadService): Service for downloading conversation data.
            repository (AbstractConversationRepository): Repository for storing and retrieving conversations.
            response_generator (AbstractResponseGeneratorService): Service for generating responses.
            tokenizer (AbstractTokenizerService): Tokenizer for managing token-related constraints.
            feedback_repo (AbstractFeedbackRepository): Repository for managing feedback data.
        """
        self._conversation_download_service = conversation_download_service
        self._repository = repository
        self._response_generator = response_generator
        self._tokenizer = tokenizer
        self._feedback_repo = feedback_repo

    def start_conversation(self) -> Conversation:
        """
        Starts a new conversation session and stores it in the repository.

        Returns:
            Conversation: A newly created Conversation instance.
        """
        conversation = Conversation.create()
        self._repository.save(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: uuid.UUID) -> Conversation:
        """
        Retrieves a conversation by its unique identifier.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.

        Returns:
            Conversation: The retrieved Conversation instance.
        """
        return self._repository.get_by_id(conversation_id)

    def add_message(self, conversation_id: uuid.UUID, message_text: str) -> Message:
        """
        Adds a new message to a specific conversation and generates a response.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            message_text (str): The text of the new message.

        Returns:
            Message: The created message instance.
        """
        conversation = self._repository.get_by_id(conversation_id)
        response = self._response_generator.generate_answer(message_text)
        conversation.add_message(message_text=message_text, response_text=response)
        self._repository.save(conversation)
        return conversation.get_last_message()

    def regenerate_or_edit_message(self, conversation_id: uuid.UUID, message_id: uuid.UUID, text: str) -> str:
        """
        Regenerates the response for a specific message in a conversation.

        Args:
            message_id (uuid.UUID): The unique ID of the conversation.
            message_id (uuid.UUID): The unique ID of the message.
            message_text (str): The new message text for the response generation.

        Returns:
            str: The regenerated response text.
        """
        conversation: Conversation = self._repository.get_by_id(conversation_id)
        new_response = self._response_generator.generate(text)
        conversation.regenerate_or_edit_message(message_id=message_id, text=text, response=new_response)
        self._repository.save(conversation)
        return new_response

    def delete_conversation(self, conversation_id: uuid.UUID) -> None:
        """
        Deletes a conversation session from the repository.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation to delete.
        """
        self._repository.delete(conversation_id=conversation_id)

    def download_conversation(self, conversation_id: uuid.UUID) -> None:
        """
        Downloads the content of a conversation using the specified download service.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation to download.
        """
        conversation = self._repository.get_by_id(conversation_id)
        self._conversation_download_service.download_conversation(conversation)

    def get_recent_messages(
        self, conversation_id: uuid.UUID, max_recent: int = 5, token_limit: int = 500
    ) -> list[Message]:
        """
        Retrieves recent messages from a conversation, respecting a token limit.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            max_recent (int, optional): The maximum number of recent messages to retrieve. Defaults to 5.
            token_limit (int, optional): The maximum token limit for the context. Defaults to 500.

        Returns:
            list[Message]: A list of recent messages within the token limit.
        """
        conversation: Conversation = self._repository.get_by_id(conversation_id)
        return conversation.get_recent_messages(max_recent=max_recent, token_limit=token_limit)

    def read_plain_message_responses(
        conversation_id: uuid.UUID, tokenizer: AbstractTokenizerService, max_recent: int = 5, token_limit: int = 500
    ) -> list[Message]:

        conversation = self._repository.get_by_id(conversation_id)

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
