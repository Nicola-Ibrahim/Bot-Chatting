from src.building_blocks.application.base_command_handler import BaseCommandHandler
from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, resultify
from src.modules.chats.domain.messages.models.feedback import Feedback
from src.modules.chats.domain.messages.models.rating import RatingType

from ....domain.interfaces.message_repository import AbstractMessageRepository
from ....infra.services import messageDTO


class AddFeedbackToMessageCommandHandler(BaseCommandHandler):
    def __init__(self, repository: AbstractMessageRepository):
        self._repository = repository

    @resultify
    def handle(self, command: AddFeedbackToMessageCommand) -> Result[messageDTO, str]:
        try:
            message = self._repository.get_by_id(command.message_id)

            feedback = Feedback.create(rating=command.rating, comment=command.comment)
            message.add_feedback_message(
                message_id=command.message_id, content_pos=command.content_pos, feedback=feedback
            )
            self._repository.save(message)

            return messageDTO.from_domain(message)

        except (BusinessRuleValidationException, RepositoryException, ValueError) as e:
            return e
