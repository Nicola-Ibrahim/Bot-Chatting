import uuid
from datetime import datetime

import pytest

from ..domain.conversations.conversation import Conversation
from ..domain.messages.rating import RatingType
from ..domain.exceptions.operation import InValidOperationException
from ..domain.value_objects.content import Content
from ..domain.value_objects.feedback import Feedback


class TestConversationLifecycle:
    def test_user_can_start_conversation(self):
        obj = Conversation.start()
        assert isinstance(obj, Conversation)

    def test_create_conversation(self, conversation):
        assert isinstance(conversation, Conversation)
        assert conversation.id is not None
        assert len(conversation.messages) == 0
        assert isinstance(conversation.created_time, datetime)

    def test_get_last_n_messages(self, conversation, content):
        conversation.add_message(content)
        second_content = Content.create(text="How are you?", response="I'm good, thanks.")
        conversation.add_message(second_content)

        last_messages = conversation.get_last_n_messages(1)
        assert len(last_messages) == 1
        assert last_messages[0].get_latest_content().text == "How are you?"

    def test_get_last_n_messages_invalid(self, conversation):
        with pytest.raises(InValidOperationException):
            conversation.get_last_n_messages(0)

    def test_get_last_n_messages_exceeding_total(self, conversation, content):
        conversation.add_message(content)
        last_messages = conversation.get_last_n_messages(5)
        assert len(last_messages) == 1
        assert last_messages[0].get_latest_content().text == content.text


def test_user_can_start_conversation():
    obj = Conversation.start()
    assert isinstance(obj, Conversation)


def test_create_conversation(conversation):
    """Test the creation of a new conversation."""
    assert isinstance(conversation, Conversation)
    assert conversation.id is not None
    assert len(conversation.messages) == 0
    assert isinstance(conversation.created_time, datetime)


def test_add_message_valid(conversation, content):
    """Test adding a valid message to the conversation."""
    message = conversation.add_message(content=content)

    # Get the latest content's text and response
    content = message.get_latest_content()

    assert len(conversation.messages) == 1
    assert content.text == "Hello what's up"
    assert content.response == "Hi there!"


def test_add_message_invalid_text(conversation):
    """Test adding a message with invalid text (less than 3 characters)."""

    with pytest.raises(InValidOperationException):
        invalid_content = Content.create(text="Hi", response="Hello what's up")
        conversation.add_message(invalid_content)


def test_add_message_invalid_response(conversation):
    """Test adding a message with invalid response (less than 3 characters)."""

    with pytest.raises(InValidOperationException):
        invalid_content = Content.create(text="Hello", response="Hi")
        conversation.add_message(invalid_content)


def test_regenerate_message_valid(conversation, content):
    """Test regenerating or editing a message with valid content."""
    message = conversation.add_message(content)

    new_content = Content.create(text="Hey", response="Hello!")
    updated_message = conversation.regenerate_or_edit_message(message.id, new_content)

    assert updated_message.get_latest_content().text == "Hey"
    assert updated_message.get_latest_content().response == "Hello!"


def test_regenerate_message_invalid(conversation, content):
    """Test regenerating or editing a message with invalid content."""
    message = conversation.add_message(content)

    with pytest.raises(InValidOperationException):
        invalid_content = Content.create(text="Hi", response="Hello")
        conversation.regenerate_or_edit_message(message.id, invalid_content)


def test_get_last_n_messages(conversation, content):
    """Test retrieving the last N messages."""
    conversation.add_message(content)

    second_content = Content.create(text="How are you?", response="I'm good, thanks.")
    conversation.add_message(second_content)

    last_messages = conversation.get_last_n_messages(1)
    assert len(last_messages) == 1
    assert last_messages[0].get_latest_content().text == "How are you?"


def test_get_last_n_messages_invalid(conversation):
    """Test retrieving last N messages with invalid number."""
    with pytest.raises(InValidOperationException):
        conversation.get_last_n_messages(0)


def test_add_feedback_to_message(conversation, content):
    """Test adding feedback to a message."""
    message = conversation.add_message(content)

    feedback = Feedback.create(rating=RatingType.LIKE, comment="Great response!")
    content = conversation.add_feedback_message(message_id=message.id, content_pos=0, feedback=feedback)

    # Validate feedback added to the specific content
    assert content.feedback.rating == RatingType.LIKE
    assert content.feedback.comment == "Great response!"


# def test_read_chat_partially(conversation, content):
#     """Test reading recent messages with token limit."""
#     tokenizer = MagicMock()
#     tokenizer.tokenize.return_value = [1] * 5  # Mocking a fixed token length for each message

#     conversation.add_message(content)

#     second_content = Content.create(text="How are you?", response="I'm good, thanks.")
#     conversation.add_message(second_content)

#     selected_messages = conversation.read_chat_partially(tokenizer, max_recent=2, token_limit=10)
#     assert len(selected_messages) == 2  # Should return 2 messages within token limit

#     selected_messages = conversation.read_chat_partially(tokenizer, max_recent=2, token_limit=5)
#     assert len(selected_messages) == 1  # Should return only 1 message within token limit


def test_message_not_found(conversation, content):
    """Test trying to regenerate or edit a message that doesn't exist."""
    non_existent_message_id = uuid.uuid4()

    with pytest.raises(InValidOperationException):
        conversation.regenerate_or_edit_message(non_existent_message_id, content)


def test_invalid_feedback(conversation):
    """Test adding feedback to a non-existent message."""
    non_existent_message_id = uuid.uuid4()

    with pytest.raises(InValidOperationException):
        feedback = Feedback.create(rating="SDFSD", comment="Great response!")
        conversation.add_feedback_message(non_existent_message_id, 0, feedback)


def test_add_feedback_invalid_content_position(conversation, content):
    """Test adding feedback to an invalid content position in a message."""
    message = conversation.add_message(content)

    feedback = Feedback.create(rating=RatingType.LIKE, comment="Great response!")

    with pytest.raises(InValidOperationException):
        conversation.add_feedback_message(message_id=message.id, content_pos=10, feedback=feedback)  # Invalid position


def test_add_feedback_invalid_rating_type(conversation, content):
    """Test adding feedback with an invalid rating type."""
    message = conversation.add_message(content)

    with pytest.raises(InValidOperationException):
        invalid_feedback = Feedback.create(rating="INVALID", comment="Bad response!")
        conversation.add_feedback_message(message_id=message.id, content_pos=0, feedback=invalid_feedback)


def test_get_last_n_messages_exceeding_total(conversation, content):
    """Test retrieving the last N messages when N exceeds total messages."""
    conversation.add_message(content)

    last_messages = conversation.get_last_n_messages(5)  # Only 1 message exists
    assert len(last_messages) == 1
    assert last_messages[0].get_latest_content().text == content.text


def test_message_with_multiple_contents(conversation):
    """Test adding multiple contents to a single message."""
    content1 = Content.create(text="Hello", response="Hi!")
    content2 = Content.create(text="How are you?", response="I'm good, thanks.")

    message = conversation.add_message(content1)
    message.add_content(content2)

    assert len(message.contents) == 2
    assert message.contents[0].text == "Hello"
    assert message.contents[1].text == "How are you?"


def test_invalid_message_id_in_feedback(conversation, content):
    """Test adding feedback to a non-existent message ID."""
    invalid_message_id = uuid.uuid4()
    feedback = Feedback.create(rating=RatingType.DISLIKE, comment="Not helpful.")

    with pytest.raises(InValidOperationException):
        conversation.add_feedback_message(message_id=invalid_message_id, content_pos=0, feedback=feedback)


def test_duplicate_messages_in_conversation(conversation, content):
    """Test adding duplicate messages with the same content."""
    message1 = conversation.add_message(content)
    message2 = conversation.add_message(content)

    assert len(conversation.messages) == 2
    assert message1 != message2  # Ensure unique message IDs


def test_message_timestamps_order(conversation, content):
    """Test that messages in a conversation are timestamped in order."""
    message1 = conversation.add_message(content)
    message2 = conversation.add_message(Content.create(text="Another message", response="Response"))

    assert message1.timestamp <= message2.timestamp
