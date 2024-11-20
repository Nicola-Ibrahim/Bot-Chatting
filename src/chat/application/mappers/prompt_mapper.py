from ...domain.value_objects.content import Content
from ..dtos.chat_dto import MessageDTO


class MessageMapper:
    """Mapper for converting between Content domain model and MessageDTO."""

    def to_dto(self, message: Content) -> MessageDTO:
        """
        Converts a Content domain model to a MessageDTO.

        Args:
            message (Content): The Content domain model.

        Returns:
            MessageDTO: Data transfer object for the Content model.
        """
        if not isinstance(message, Content):
            raise TypeError(f"Expected Content instance, got {type(message).__name__}")
        return MessageDTO(id=message.id, question=message.text, answer=message.response)

    def from_dto(self, message_dto: MessageDTO) -> Content:
        """
        Converts a MessageDTO to a Content domain model.

        Args:
            message_dto (MessageDTO): The Content data transfer object.

        Returns:
            Content: Domain model for the Content.
        """
        if not isinstance(message_dto, MessageDTO):
            raise TypeError(f"Expected MessageDTO instance, got {type(message_dto).__name__}")
        return Content(id=message_dto.id, text=message_dto.question, response=message_dto.answer)
