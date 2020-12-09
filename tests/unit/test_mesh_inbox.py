import logging
from unittest import mock

import pytest

from s3mesh.mesh import MESH_MESSAGE_TYPE_DATA, MESH_STATUS_EVENT_TRANSFER, MESH_STATUS_SUCCESS
from tests.builders.common import a_string
from tests.builders.mesh import build_mex_headers, mock_client_message, mock_mesh_inbox


def test_returns_messages():
    message_ids = [a_string(), a_string(), a_string()]
    client_messages = [mock_client_message(message_id=m_id) for m_id in message_ids]
    mesh_inbox = mock_mesh_inbox(client_messages=client_messages)

    actual_messages_ids = [message.id for message in mesh_inbox.read_messages()]

    assert actual_messages_ids == message_ids


def test_catches_exception():
    unsuccessful_message = mock_client_message(
        mex_headers=build_mex_headers(status_event="COLLECT")
    )
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    actual_messages = list(mesh_inbox.read_messages())
    expected_messages = []

    assert actual_messages == expected_messages


def test_continues_reading_messages_when_one_of_them_has_invalid_mesh_header():
    successful_message_1 = mock_client_message(message_id=a_string())
    successful_message_2 = mock_client_message(message_id=a_string())
    unsuccessful_message = mock_client_message(
        message_id=a_string(), mex_headers=build_mex_headers(status_success="ERROR")
    )

    client_messages = [successful_message_1, unsuccessful_message, successful_message_2]
    mesh_inbox = mock_mesh_inbox(client_messages=client_messages)

    actual_message_ids = [message.id for message in mesh_inbox.read_messages()]
    expected_message_ids = [successful_message_1.id(), successful_message_2.id()]

    assert actual_message_ids == expected_message_ids


def test_continues_reading_messages_when_one_of_them_has_missing_mesh_header():
    successful_message_1 = mock_client_message(message_id=a_string())
    successful_message_2 = mock_client_message(message_id=a_string())
    missing_mex_headers = build_mex_headers()
    del missing_mex_headers["filename"]
    unsuccessful_message = mock_client_message(
        message_id=a_string(), mex_headers=missing_mex_headers
    )

    client_messages = [successful_message_1, unsuccessful_message, successful_message_2]
    mesh_inbox = mock_mesh_inbox(client_messages=client_messages)

    actual_message_ids = [message.id for message in mesh_inbox.read_messages()]
    expected_message_ids = [successful_message_1.id(), successful_message_2.id()]

    assert actual_message_ids == expected_message_ids


def test_does_not_catch_generic_exception():
    unsuccessful_message = mock_client_message()
    unsuccessful_message.id.side_effect = Exception()
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    with pytest.raises(Exception):
        list(mesh_inbox.read_messages())


def test_calls_logger_with_a_warning_when_header_statussuccess_is_not_success():
    logger = logging.getLogger("s3mesh.mesh")
    message_id = a_string()
    error_status = "ERROR"
    unsuccessful_message = mock_client_message(
        message_id=message_id, mex_headers=build_mex_headers(status_success=error_status)
    )
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    with mock.patch.object(logger, "warning") as mock_warn:
        list(mesh_inbox.read_messages())

    mock_warn.assert_called_with(
        f"Message {message_id}: "
        f"Invalid MESH statussuccess header - expected: {MESH_STATUS_SUCCESS}, "
        f"instead got: {error_status}"
    )


def test_calls_logger_with_a_warning_when_header_messagetype_is_not_data():
    logger = logging.getLogger("s3mesh.mesh")
    message_id = a_string()
    message_type = "TEXT"
    unsuccessful_message = mock_client_message(
        message_id=message_id, mex_headers=build_mex_headers(message_type=message_type)
    )
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    with mock.patch.object(logger, "warning") as mock_warn:
        list(mesh_inbox.read_messages())

    mock_warn.assert_called_with(
        f"Message {message_id}: "
        f"Invalid MESH messagetype header - expected: {MESH_MESSAGE_TYPE_DATA}, "
        f"instead got: {message_type}"
    )


def test_calls_logger_with_a_warning_when_header_statusevent_is_not_transfer():
    logger = logging.getLogger("s3mesh.mesh")
    message_id = a_string()
    statusevent = "UPLOAD"
    unsuccessful_message = mock_client_message(
        message_id=message_id, mex_headers=build_mex_headers(status_event=statusevent)
    )
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    with mock.patch.object(logger, "warning") as mock_warn:
        list(mesh_inbox.read_messages())

    mock_warn.assert_called_with(
        f"Message {message_id}: "
        f"Invalid MESH statusevent header - expected: {MESH_STATUS_EVENT_TRANSFER}, "
        f"instead got: {statusevent}"
    )


@pytest.mark.parametrize(
    "missing_header_name",
    ["filename", "statustimestamp", "statusevent", "statussuccess", "messagetype"],
)
def test_calls_logger_with_a_warning_when_required_mex_header_is_missing(missing_header_name):
    logger = logging.getLogger("s3mesh.mesh")
    message_id = a_string()
    mex_headers = build_mex_headers()
    del mex_headers[missing_header_name]
    unsuccessful_message = mock_client_message(message_id=message_id, mex_headers=mex_headers)
    mesh_inbox = mock_mesh_inbox(client_messages=[unsuccessful_message])

    with mock.patch.object(logger, "warning") as mock_warn:
        list(mesh_inbox.read_messages())

    mock_warn.assert_called_with(
        f"Message {message_id}: " f"Missing MESH {missing_header_name} header"
    )
