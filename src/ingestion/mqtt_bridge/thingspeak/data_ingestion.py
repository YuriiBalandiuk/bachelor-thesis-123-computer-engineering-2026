from copy import deepcopy

from src.ingestion.wrapper.mqtt_wrapper import MQTTClientWrapper
from src.ingestion.mqtt_bridge.thingspeak.endpoint_config import MQTT_SUBSCRIPTION


mqtt_client = MQTTClientWrapper(deepcopy(MQTT_SUBSCRIPTION["channels_thingspeak"]))
mqtt_client.start()