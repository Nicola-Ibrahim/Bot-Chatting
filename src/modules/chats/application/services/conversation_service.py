import uuid

from ....domain.primitive.exception import BusinessRuleValidationException
from ....domain.primitive.result import Result
from ...domain.conversations.conversation import Conversation
from ...domain.messages.rating import RatingType
from ...domain.value_objects.content import Content
from ...domain.value_objects.feedback import Feedback
from ...infra.persistence.exceptions import RepositoryException
from ..contracts.conversation import ConversationDTO
from ..interfaces.conversation_repository import AbstractConversationRepository
from ..interfaces.downloader import AbstractConversationDownloader


class ConversationApplicationService:
    """
    Orchestrator for managing conversation-related operations. This class handles messages
    between domain models, domain services, and infrastructure services. It provides
    a high-level interface for starting, updating, retrieving, and managing conversations
    while delegating domain logic to specific domain entities and services.
    """

    def __init__(
        self,
        conversation_downloader: AbstractConversationDownloader,
        repository: AbstractConversationRepository,
        response_generator,
        tokenizer,
    ):
        """
        Initializes the gateway with necessary services and repositories.

        Args:
            conversation_downloader (ConversationDownloader): Service for downloading conversation data.
            repository (AbstractConversationRepository): Repository for storing and retrieving conversations.
        """
        self._conversation_downloader = conversation_downloader
        self._repository = repository
        self._response_generator = response_generator
        self._tokenizer = tokenizer

    def add_feedback_to_message(
        self,
        conversation_id: uuid.UUID,
        message_id: uuid.UUID,
        content_pos: int,
        rating: RatingType,
        comment: str,
    ) -> Result:
        """
        Adds feedback to a specific message within a conversation.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation.
            message_id (uuid.UUID): The unique ID of the message.
            rating (RatingType): The rating provided in the feedback.
            comment (str): The optional comment for the feedback.

        Returns:
            Result: A Result indicating the outcome of the operation.
        """
        try:
            conversation = self._repository.get_by_id(conversation_id)
            if not conversation:
                return Result.fail(RepositoryException.entity_not_found("Conversation not found."))

            feedback = Feedback.create(rating=rating, comment=comment)
            conversation.add_feedback_message(message_id=message_id, content_pos=content_pos, feedback=feedback)
            self._repository.save(conversation)
            return Result.ok(ConversationDTO.from_domain(conversation))
        except BusinessRuleValidationException as e:
            return Result.fail(e)

    def download(self, conversation_id: uuid.UUID) -> Result:
        """
        Downloads the content of a conversation using the specified download service.

        Args:
            conversation_id (uuid.UUID): The unique ID of the conversation to download.

        Returns:
            Result: A Result indicating the outcome of the download operation.
        """
        try:
            conversation = self._repository.get_by_id(conversation_id)
            if not conversation:
                return Result.fail(RepositoryException.entity_not_found("Conversation not found."))

            self._conversation_downloader.download(conversation)
            return Result.ok(None)
        except BusinessRuleValidationException as e:
            return Result.fail(e)
