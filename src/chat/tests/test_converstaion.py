from ..domain.entities.conversation import Conversation
from ..domain.value_objects.content import Content
from ..domain.value_objects.feedback import Feedback


def test_user_can_start_conversation():

    conversation = Conversation.start()

    assert isinstance(conversation, Conversation)
