import pytest

from ..domain.exceptions.operation import InValidOperationException
from ..domain.value_objects.content import Content


class TestMessageOperations:
    def test_add_message_valid(self, conversation, content):
        message = conversation.add_message(content=content)
        content = message.get_latest_content()
        assert len(conversation.messages) == 1
        assert content.text == "Hello what's up"
        assert content.response == "Hi there!"

    def test_add_message_invalid_text(self, conversation):
        with pytest.raises(InValidOperationException):
            invalid_content = Content.create(text="Hi", response="Hello what's up")
            conversation.add_message(invalid_content)

    def test_add_message_invalid_response(self, conversation):
        with pytest.raises(InValidOperationException):
            invalid_content = Content.create(text="Hello", response="Hi")
            conversation.add_message(invalid_content)

    def test_message_timestamps_order(self, conversation, content):
        message1 = conversation.add_message(content)
        message2 = conversation.add_message(Content.create(text="Another message", response="Response"))
        assert message1.timestamp <= message2.timestamp

    def test_duplicate_messages_in_conversation(self, conversation, content):
        message1 = conversation.add_message(content)
        message2 = conversation.add_message(content)
        assert len(conversation.messages) == 2
        assert message1 != message2
