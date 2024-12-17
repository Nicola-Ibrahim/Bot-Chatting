from uuid import UUID

from pydantic import BaseModel, Field

from ....domain import AbstractConversationRepository
from ..domain.entities.conversation import Conversation
from ..domain.exceptions import RepositoryException
from ..domain.value_objects.content import Content
from ..dto import ConversationDTO
from .result import Result


class AddMessageToConversationCommand(BaseModel):
    conversation_id: UUID
    text: str = Field(..., min_length=1, max_length=5000)

    class Config:
        schema_extra = {
            "example": {"conversation_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "text": "Hello, how are you?"}
        }


class AddMessageToConversationCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractConversationRepository, response_generator: ResponseGenerator):
        self._repository = repository
        self._response_generator = response_generator

    def handle(self, command: AddMessageCommand) -> Result:
        try:
            conversation = self._repository.get_by_id(command.conversation_id)
            if not conversation:
                return Result.fail("Conversation not found.")

            response = self._response_generator.generate_answer(command.text)
            if not response:
                return Result.fail("Failed to generate a response.")

            content = Content.create(text=command.text, response=response)
            conversation.add_message(content=content)
            self._repository.save(conversation)
            return Result.ok(ConversationDTO.from_domain(conversation))
        except Exception as e:
            return Result.fail(str(e))

    def _publish_event(self, event):
        # Event dispatcher logic to handle domain events (to be implemented)
        pass
