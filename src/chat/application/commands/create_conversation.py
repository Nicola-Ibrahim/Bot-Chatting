from ....domain.primitive.result import Result
from ...application.services.conversation_dto import ConversationDTO
from ...infra.persistence.exceptions import RepositoryException
from ..interfaces.conversation_repository import AbstractConversationRepository


class CreateConversationCommandHandler:
    def __init__(self, repository: AbstractConversationRepository):
        self._repository = repository

    def execute(self) -> Result:
        try:
            conversation = Conversation.start()
            self._repository.save(conversation)
            return Result.ok(ConversationDTO.from_domain(conversation))
        except RepositoryException as e:
            return Result.fail(str(e))
