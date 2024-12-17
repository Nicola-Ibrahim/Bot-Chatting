import uuid

from pydantic import BaseModel, Field

from ....domain.primitive.result import Result
from ...domain.conversations.IRepository import AbstractConversationRepository
from ...infra.persistence.exceptions import RepositoryException
from ..services import ConversationDTO


class AddMessageCommand(BaseModel):
    user_id: uuid.UUID


class GetAllConversationCommandHandler(BaseQueryHandler):
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    def handle(self, query: GetConversationByIdQuery) -> Result:
        try:
            conversation = self._repository.get_by_id(query.conversation_id)
            if not conversation:
                return Result.fail("Conversation not found.")
            return Result.ok(ConversationDTO.from_domain(conversation))
        except Exception as e:
            return Result.fail(str(e))
