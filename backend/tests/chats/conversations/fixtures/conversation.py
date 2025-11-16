import pytest

from ...domain.conversations.conversation import Conversation


@pytest.fixture
def conversation():
    return Conversation.start()
