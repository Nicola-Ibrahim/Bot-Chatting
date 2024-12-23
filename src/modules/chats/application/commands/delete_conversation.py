import uuid

from pydantic import BaseModel

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify

from ....domain.interfaces.conversation_repository import AbstractConversationRepository


class DeleteConversationCommand(BaseModel):
    conversation_id: uuid.UUID

    class Config:
        schema_extra = {"example": {"conversation_id": "123e4567-e89b-12d3-a456-426614174000"}}


class DeleteConversationCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    @resultify
    def handle(self, command: DeleteConversationCommand) -> Result[None, str]:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)

            self._repository.delete(command.conversation_id)
            return None
        except (BusinessRuleValidationException, RepositoryException) as e:
            return e
