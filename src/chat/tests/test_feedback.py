import uuid

import pytest

from ..domain.enums.rating import RatingType
from ..domain.exceptions.operation import InValidOperationException
from ..domain.value_objects.feedback import Feedback


class TestFeedbackOperations:
    def test_add_feedback_to_message(self, conversation, content):
        message = conversation.add_message(content)
        feedback = Feedback.create(rating=RatingType.LIKE, comment="Great response!")
        content = conversation.add_feedback_message(message_id=message.id, content_pos=0, feedback=feedback)
        assert content.feedback.rating == RatingType.LIKE
        assert content.feedback.comment == "Great response!"

    def test_invalid_feedback(self, conversation):
        non_existent_message_id = uuid.uuid4()
        with pytest.raises(InValidOperationException):
            feedback = Feedback.create(rating="SDFSD", comment="Great response!")
            conversation.add_feedback_message(non_existent_message_id, 0, feedback)

    def test_add_feedback_invalid_content_position(self, conversation, content):
        message = conversation.add_message(content)
        feedback = Feedback.create(rating=RatingType.LIKE, comment="Great response!")
        with pytest.raises(InValidOperationException):
            conversation.add_feedback_message(message_id=message.id, content_pos=10, feedback=feedback)

    def test_add_feedback_invalid_rating_type(self, conversation, content):
        message = conversation.add_message(content)
        with pytest.raises(InValidOperationException):
            invalid_feedback = Feedback.create(rating="INVALID", comment="Bad response!")
            conversation.add_feedback_message(message_id=message.id, content_pos=0, feedback=invalid_feedback)

    def test_invalid_message_id_in_feedback(self, conversation, content):
        invalid_message_id = uuid.uuid4()
        feedback = Feedback.create(rating=RatingType.DISLIKE, comment="Not helpful.")
        with pytest.raises(InValidOperationException):
            conversation.add_feedback_message(message_id=invalid_message_id, content_pos=0, feedback=feedback)
