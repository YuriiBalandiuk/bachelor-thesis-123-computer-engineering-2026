import logging
from copy import deepcopy

from src.logging_config import setup_logging
from src.ingestion.wrapper.mqtt_wrapper import MQTTClientWrapper
from src.ingestion.mqtt_bridge.thingspeak.endpoint_config import MQTT_SUBSCRIPTION

setup_logging(__name__)

logger = logging.getLogger(__name__)


def run() -> None:
    """
    Start MQTT subscription broker.

    Initializes the MQTT client using predefined configuration
    and starts message consumption loop.

    Raises:
        Exception: Propagates initialization or runtime errors
            from the MQTT client.
    """
    try:
        mqtt_client = MQTTClientWrapper(
            deepcopy(MQTT_SUBSCRIPTION["channels_thingspeak"])
        )
        mqtt_client.start()
    except Exception as e:
        logging.error(f"Unable to start fetch data - {e}", exc_info=True)

if __name__ == "__main__":
    run()
