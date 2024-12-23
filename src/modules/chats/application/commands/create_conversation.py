import uuid

from pydantic import BaseModel

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.root import Conversation

from ....domain.interfaces.conversation_repository import AbstractConversationRepository
from ...application.services.conversation_dto import ConversationDTO
from ...infra.persistence.exceptions import RepositoryException


class CreateConversationCommand(BaseModel):
    user_id: uuid.UUID

    class Config:
        schema_extra = {"example": {"user_id": "123e4567-e89b-12d3-a456-426614174000"}}


class CreateNewConversationCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: CreateConversationCommand) -> Result[ConversationDTO, str]:
        try:
            conversation = Conversation.start(user_id=command.user_id)
            self._repository.save(conversation)
            return ConversationDTO.from_domain(conversation)
        except (BusinessRuleValidationException, RepositoryException) as e:
            return e
