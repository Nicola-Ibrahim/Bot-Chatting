import pytest

from ...domain.entities.conversation import Conversation


@pytest.fixture
def conversation():
    return Conversation.start()
