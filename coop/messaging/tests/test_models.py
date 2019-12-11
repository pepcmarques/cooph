import pytest

from coop.messaging.models import Message
from coop.messaging.models import MessageChoice


@pytest.mark.parametrize(
    "task", [MessageChoice.choices()[0][0]]
)
def test_messaging_model(client, task):
    message = Message()
    message.task = task
    assert str(message) == task
