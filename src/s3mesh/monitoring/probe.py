from logging import Logger, getLogger

from s3mesh.monitoring.event.count import CountMessagesEvent
from s3mesh.monitoring.event.forward import ForwardMessageEvent
from s3mesh.monitoring.event.poll import PollMessagesEvent
from s3mesh.monitoring.output import LoggingOutput

logger = getLogger(__name__)


class LoggingProbe:
    def __init__(self, log: Logger = logger):
        self._output = LoggingOutput(log)

    def new_count_messages_event(self) -> CountMessagesEvent:
        return CountMessagesEvent(self._output)

    def new_poll_messages_event(self) -> PollMessagesEvent:
        return PollMessagesEvent(self._output)

    def new_forward_message_event(self) -> ForwardMessageEvent:
        return ForwardMessageEvent(self._output)
