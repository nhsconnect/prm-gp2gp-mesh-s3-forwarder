from logging import Logger


class LoggingOutput:
    def __init__(self, log: Logger):
        self._logger = log

    def log_event(self, event_name, fields):
        self._logger.info(f"Observed {event_name}", extra=fields)
