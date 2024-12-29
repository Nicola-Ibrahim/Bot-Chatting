from src.building_blocks.domain.exception import BusinessRuleValidationException, RepositoryException
from src.building_blocks.domain.result import Result, TError, resultify
from src.modules.chats.domain.messages.models.feedback import Feedback

from ....domain.interfaces.message_repository import AbstractMessageRepository
from ....domain.messages.root import Message
from ...configuration.command_handler import AbstractCommandHandler
from .add_feedback_to_message_command import AddFeedbackToMessageCommand


class AddFeedbackToMessageCommandHandler(AbstractCommandHandler[AddFeedbackToMessageCommand, Result[Message, TError]]):
    def __init__(self, repository: AbstractMessageRepository):
        self._repository = repository

    @resultify
    def handle(self, command: AddFeedbackToMessageCommand) -> Result[Message, TError]:
        # The Result type encapsulates either a successful result (Message) or an error of type TError
        try:
            message = self._repository.get_by_id(command.message_id)

            feedback = Feedback.create(rating=command.rating, comment=command.comment)
            message.add_feedback_message(
                message_id=command.message_id, content_pos=command.content_pos, feedback=feedback
            )
            self._repository.save(message)

            return message

        except (BusinessRuleValidationException, RepositoryException, ValueError) as e:
            return e
