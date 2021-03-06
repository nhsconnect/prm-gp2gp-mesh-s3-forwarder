from s3mesh.mesh import InvalidMeshHeader, MeshMessage, MissingMeshHeader
from s3mesh.monitoring.error import INVALID_MESH_HEADER_ERROR, MISSING_MESH_HEADER_ERROR
from s3mesh.monitoring.event.base import ForwarderEvent

FORWARD_MESSAGE_EVENT = "FORWARD_MESH_MESSAGE"


class ForwardMessageEvent(ForwarderEvent):
    def __init__(self, output):
        super().__init__(output, FORWARD_MESSAGE_EVENT)

    def record_message_metadata(self, message: MeshMessage):
        self._fields["messageId"] = message.id
        self._fields["sender"] = message.sender
        self._fields["recipient"] = message.recipient
        self._fields["fileName"] = message.file_name

    def record_s3_key(self, key):
        self._fields["s3Key"] = key

    def record_missing_mesh_header(self, exception: MissingMeshHeader):
        self._fields["error"] = MISSING_MESH_HEADER_ERROR
        self._fields["missingHeaderName"] = exception.header_name

    def record_invalid_mesh_header(self, exception: InvalidMeshHeader):
        self._fields["error"] = INVALID_MESH_HEADER_ERROR
        self._fields["headerName"] = exception.header_name
        self._fields["expectedHeaderValue"] = exception.expected_header_value
        self._fields["receivedHeaderValue"] = exception.header_value
