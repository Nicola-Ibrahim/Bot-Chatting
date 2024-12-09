import pytest

from ...domain.value_objects.content import Content


@pytest.fixture
def content():
    return Content.create(text="Hello what's up", response="Hi there!")
