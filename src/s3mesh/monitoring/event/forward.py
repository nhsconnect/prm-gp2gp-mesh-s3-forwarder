from s3mesh.mesh import InvalidMeshHeader, MeshClientNetworkError, MeshMessage, MissingMeshHeader
from s3mesh.monitoring.error import (
    INVALID_MESH_HEADER_ERROR,
    MESH_CLIENT_NETWORK_ERROR,
    MISSING_MESH_HEADER_ERROR,
)
from s3mesh.monitoring.output import LoggingOutput

FORWARD_MESSAGE_EVENT = "FORWARD_MESH_MESSAGE"


class ForwardMessageEvent:
    def __init__(self, output: LoggingOutput):
        self._fields = {}
        self._output = output

    def record_message_metadata(self, message: MeshMessage):
        self._fields["messageId"] = message.id
        self._fields["sender"] = message.sender
        self._fields["recipient"] = message.recipient
        self._fields["fileName"] = message.file_name

    def record_s3_key(self, s3_key: str):
        self._fields["s3Key"] = s3_key

    def record_missing_mesh_header(self, exception: MissingMeshHeader):
        self._fields["error"] = MISSING_MESH_HEADER_ERROR
        self._fields["missingHeaderName"] = exception.header_name

    def record_invalid_mesh_header(self, exception: InvalidMeshHeader):
        self._fields["error"] = INVALID_MESH_HEADER_ERROR
        self._fields["expectedHeaderValue"] = exception.expected_header_value
        self._fields["receivedHeaderValue"] = exception.header_value

    def record_mesh_client_network_error(self, exception: MeshClientNetworkError):
        self._fields["error"] = MESH_CLIENT_NETWORK_ERROR
        self._fields["errorMessage"] = exception.error_message

    def finish(self):
        self._output.log_event(FORWARD_MESSAGE_EVENT, self._fields)
