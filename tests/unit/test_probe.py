import logging
from unittest.mock import MagicMock, call, patch


def test_observation_receives_name_from_probe():
    event_name = "an_event"
    probe = LoggingProbe()
    observation = probe.start_observation(event_name)

    logger = logging.getLogger("s3mesh.probe")
    with patch.object(logger, "info") as mock_info:
        observation.finish()

    mock_info.assert_called_once_with(f"Observed {event_name}", extra={"event": event_name})


def test_logs_single_observation():
    event_name = "an_event"
    logger = MagicMock()
    observation = LoggingObservation(event_name, logger)

    observation.add_field("vegetable", "turnip")

    observation.finish()

    logger.info.assert_has_calls(
        [call.info(f"Observed {event_name}", extra={"vegetable": "turnip", "event": event_name})],
        any_order=False,
    )


def test_logs_multiple_observations():
    event_name = "an_event"
    logger = MagicMock()
    observation = LoggingObservation(event_name, logger)

    observation.add_field("vegetable", "turnip")
    observation.add_field("fruit", "mango")

    observation.finish()

    logger.info.assert_has_calls(
        [
            call.info(
                f"Observed {event_name}",
                extra={"vegetable": "turnip", "fruit": "mango", "event": event_name},
            )
        ],
        any_order=False,
    )
