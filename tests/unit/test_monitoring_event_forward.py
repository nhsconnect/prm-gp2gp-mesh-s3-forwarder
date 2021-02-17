from mock import MagicMock

from s3mesh.monitoring.event.forward import FORWARD_MESSAGE_EVENT, ForwardMessageEvent
from tests.builders.mesh import mock_mesh_message


def test_finish_calls_log_event_with_event_name():
    mock_output = MagicMock()

    forward_message_event = ForwardMessageEvent(mock_output)
    forward_message_event.finish()

    mock_output.log_event.assert_called_with(FORWARD_MESSAGE_EVENT, {})


def test_record_message_metadata():
    mock_output = MagicMock()
    message = mock_mesh_message()

    forward_message_event = ForwardMessageEvent(mock_output)
    forward_message_event.record_message_metadata(message)
    forward_message_event.finish()

    mock_output.log_event.assert_called_with(
        FORWARD_MESSAGE_EVENT,
        {
            "messageId": message.id,
            "sender": message.sender,
            "recipient": message.recipient,
            "fileName": message.file_name,
        },
    )
