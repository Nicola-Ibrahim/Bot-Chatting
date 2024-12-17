from app.application.commands.add_feedback import AddFeedbackCommand, AddFeedbackCommandHandler
from app.application.commands.add_message import AddMessageCommand, AddMessageCommandHandler
from app.application.commands.create_conversation import CreateConversationCommand, CreateConversationCommandHandler
from app.application.queries.get_conversation import GetConversationByIdQuery, GetConversationByIdQueryHandler
from app.infra.persistence.conversation_repository import (
    ConversationRepository,  # Assuming you have a repository class
)
from fastapi import APIRouter, Depends

router = APIRouter()

# Dependency Injection for command handlers
conversation_repository = ConversationRepository()  # Example repo
response_generator = ResponseGenerator()  # Example generator

create_conversation_handler = CreateConversationCommandHandler(conversation_repository)
add_message_handler = AddMessageCommandHandler(conversation_repository, response_generator)
add_feedback_handler = AddFeedbackCommandHandler(conversation_repository)
get_conversation_handler = GetConversationByIdQueryHandler(conversation_repository)


@router.post("/conversations")
def create_conversation():
    command = CreateConversationCommand()
    return create_conversation_handler.execute(command)


@router.post("/conversations/{conversation_id}/messages")
def add_message(conversation_id: uuid.UUID, text: str):
    command = AddMessageCommand(conversation_id=conversation_id, text=text)
    return add_message_handler.execute(command)


@router.post("/conversations/{conversation_id}/messages/{message_id}/feedback")
def add_feedback(
    conversation_id: uuid.UUID, message_id: uuid.UUID, content_pos: int, rating: RatingType, comment: str
):
    command = AddFeedbackCommand(
        conversation_id=conversation_id, message_id=message_id, content_pos=content_pos, rating=rating, comment=comment
    )
    return add_feedback_handler.execute(command)


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: uuid.UUID):
    query = GetConversationByIdQuery(conversation_id=conversation_id)
    return get_conversation_handler.execute(query)
