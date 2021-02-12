from s3mesh.mesh import MeshClientNetworkError
from s3mesh.monitoring.error import MESH_CLIENT_NETWORK_ERROR
from s3mesh.monitoring.output import LoggingOutput

POLL_MESSAGE_EVENT = "POLL_MESSAGE"


class PollMessagesEvent:
    def __init__(self, output: LoggingOutput):
        self._fields = {}
        self._output = output

    def record_message_batch_count(self, count: int):
        self._fields["batchMessageCount"] = count

    def record_mesh_client_network_error(self, exception: MeshClientNetworkError):
        self._fields["error"] = MESH_CLIENT_NETWORK_ERROR
        self._fields["errorMessage"] = exception.error_message

    def finish(self):
        self._output.log_event(POLL_MESSAGE_EVENT, self._fields)
