import pytest

from ..domain.exceptions.operation import InValidOperationException
from ..domain.value_objects.content import Content


class TestContentOperations:
    def test_regenerate_message_valid(self, conversation, content):
        message = conversation.add_message(content)
        new_content = Content.create(text="Hey", response="Hello!")
        updated_message = conversation.regenerate_or_edit_message(message.id, new_content)
        assert updated_message.get_latest_content().text == "Hey"
        assert updated_message.get_latest_content().response == "Hello!"

    def test_regenerate_message_invalid(self, conversation, content):
        message = conversation.add_message(content)
        with pytest.raises(InValidOperationException):
            invalid_content = Content.create(text="Hi", response="Hello")
            conversation.regenerate_or_edit_message(message.id, invalid_content)

    def test_message_with_multiple_contents(self, conversation):
        content1 = Content.create(text="Hello", response="Hi!")
        content2 = Content.create(text="How are you?", response="I'm good, thanks.")
        message = conversation.add_message(content1)
        message.add_content(content2)
        assert len(message.contents) == 2
        assert message.contents[0].text == "Hello"
        assert message.contents[1].text == "How are you?"
