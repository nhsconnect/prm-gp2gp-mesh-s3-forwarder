import logging
from datetime import datetime
from typing import Iterable

from mesh_client import MeshClient, Message

MESH_STATUS_EVENT_TRANSFER = "TRANSFER"
MESH_MESSAGE_TYPE_DATA = "DATA"
MESH_STATUS_SUCCESS = "SUCCESS"

logger = logging.getLogger(__name__)


class MeshMessage:
    def __init__(self, client_message: Message):
        self.id: str = client_message.id()
        self._client_message: Message = client_message

    def _read_header(self, header_name: str):
        try:
            return self._client_message.mex_header(header_name)
        except KeyError:
            raise MissingMeshHeader(header_name=header_name)

    @property
    def file_name(self) -> str:
        return self._read_header("filename")

    @property
    def date_delivered(self) -> datetime:
        date_header = self._read_header("statustimestamp")
        return datetime.strptime(date_header, "%Y%m%d%H%M%S")

    def validate(self):
        if (header_value := self._read_header("statusevent").upper()) != MESH_STATUS_EVENT_TRANSFER:
            raise UnexpectedStatusEvent(header_value)
        if (header_value := self._read_header("statussuccess").upper()) != MESH_STATUS_SUCCESS:
            raise UnsuccessfulStatus(header_value)
        if (header_value := self._read_header("messagetype").upper()) != MESH_MESSAGE_TYPE_DATA:
            raise UnexpectedMessageType(header_value)

    def acknowledge(self):
        self._client_message.acknowledge()

    def read(self, n=None):
        return self._client_message.read(n)


class MeshInbox:
    def __init__(self, client: MeshClient):
        self._client = client

    def read_messages(self) -> Iterable[MeshMessage]:
        for client_message in self._client.iterate_all_messages():
            yield MeshMessage(client_message)


class InvalidMeshHeader(Exception):
    def __init__(self, header_name: str, header_value: str, expected_header_value: str):
        self.header_name = header_name
        self.header_value = header_value
        self.expected_header_value = expected_header_value


class UnexpectedStatusEvent(InvalidMeshHeader):
    def __init__(self, status_event_header):
        super().__init__(
            header_name="statusevent",
            header_value=status_event_header,
            expected_header_value=MESH_STATUS_EVENT_TRANSFER,
        )


class UnsuccessfulStatus(InvalidMeshHeader):
    def __init__(self, status_success_header):
        super().__init__(
            header_name="statussuccess",
            header_value=status_success_header,
            expected_header_value=MESH_STATUS_SUCCESS,
        )


class UnexpectedMessageType(InvalidMeshHeader):
    def __init__(self, message_type_header):
        super().__init__(
            header_name="messagetype",
            header_value=message_type_header,
            expected_header_value=MESH_MESSAGE_TYPE_DATA,
        )


class MissingMeshHeader(Exception):
    def __init__(
        self,
        header_name: str,
    ):
        self.header_name = header_name
