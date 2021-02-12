from typing import Dict

from s3mesh.mesh import MeshClientNetworkError
from s3mesh.monitoring.error import MESH_CLIENT_NETWORK_ERROR
from s3mesh.monitoring.output import LoggingOutput

COUNT_MESSAGES_EVENT = "COUNT_MESSAGES"


class CountMessagesEvent:
    def __init__(self, output: LoggingOutput):
        self._fields = {}
        self._output = output

    def record_message_count(self, count: int):
        self._fields["inboxMessageCount"] = count

    def record_mesh_client_network_error(self, exception: MeshClientNetworkError):
        self._fields["error"] = MESH_CLIENT_NETWORK_ERROR
        self._fields["errorMessage"] = exception.error_message

    def finish(self):
        self._output.log_event(COUNT_MESSAGES_EVENT, self._fields)
