from uuid import UUID

from pydantic import BaseModel, Field

from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.conversations.root import Conversation
from src.modules.chats.domain.messages.root import Message
from src.modules.chats.domain.value_objects import Content


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

    @resultify
    def handle(self, command: AddMessageCommand) -> Result[ConversationDTO, str]:
        try:
            response = self._response_generator.generate_answer(command.text)

            content = Content.create(text=command.text, response=response)
            conversation.add_message(content=content)
            Message.create(content=content)
            self._repository.save(conversation)

            return ConversationDTO.from_domain(conversation)

        except (BusinessRuleValidationException, RepositoryException) as e:
            return e

    def _publish_event(self, event):
        # Event dispatcher logic to handle domain events (to be implemented)
        pass
