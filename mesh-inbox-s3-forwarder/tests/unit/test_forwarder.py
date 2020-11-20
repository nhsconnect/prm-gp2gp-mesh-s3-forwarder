from unittest.mock import MagicMock, call

from s3mesh.forwarder import MeshToS3Forwarder


def test_forwards_message():
    mock_mesh_inbox = MagicMock()
    mock_s3_uploader = MagicMock()
    mock_mesh_message = MagicMock()
    mock_mesh_inbox.read_messages.return_value = iter([mock_mesh_message])
    forwarder = MeshToS3Forwarder(mock_mesh_inbox, mock_s3_uploader)

    forwarder.forward_messages()

    mock_s3_uploader.upload.assert_called_once_with(mock_mesh_message)


def test_acknowledges_message():
    mock_mesh_inbox = MagicMock()
    mock_s3_uploader = MagicMock()
    mock_mesh_message = MagicMock()
    mock_mesh_inbox.read_messages.return_value = iter([mock_mesh_message])
    forwarder = MeshToS3Forwarder(mock_mesh_inbox, mock_s3_uploader)

    forwarder.forward_messages()

    mock_mesh_message.acknowledge.assert_called_once()


def test_forwards_multiple_messages():
    mock_mesh_inbox = MagicMock()
    mock_s3_uploader = MagicMock()
    mock_mesh_message_one = MagicMock()
    mock_mesh_message_two = MagicMock()
    mock_mesh_messages = [mock_mesh_message_one, mock_mesh_message_two]
    mock_mesh_inbox.read_messages.return_value = iter(mock_mesh_messages)
    forwarder = MeshToS3Forwarder(mock_mesh_inbox, mock_s3_uploader)

    forwarder.forward_messages()

    mock_s3_uploader.upload.assert_has_calls(
        [
            call(mock_mesh_message_one),
            call(mock_mesh_message_two),
        ]
    )

    assert mock_s3_uploader.upload.call_count == 2


def test_acknowledges_multiple_message():
    mock_mesh_inbox = MagicMock()
    mock_s3_uploader = MagicMock()
    mock_mesh_messages = [MagicMock(), MagicMock()]
    mock_mesh_inbox.read_messages.return_value = iter(mock_mesh_messages)
    forwarder = MeshToS3Forwarder(mock_mesh_inbox, mock_s3_uploader)

    forwarder.forward_messages()

    for mock_mesh_message in mock_mesh_messages:
        mock_mesh_message.acknowledge.assert_called_once()
