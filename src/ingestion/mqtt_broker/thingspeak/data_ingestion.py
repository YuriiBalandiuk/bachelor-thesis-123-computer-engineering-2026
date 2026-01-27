# import paho.mqtt.client as mqtt
from copy import deepcopy

from src.ingestion.wrapper.mqtt_wrapper import MQTTClientWrapper
from src.ingestion.mqtt_broker.thingspeak.endpoint_config import MQTT_SUBSCRIPTION


def data_ingestion_by_mqtt(configs: dict) -> dict:
    """
    TODO
    """
    clients = {}

    for name, cfg in deepcopy(configs).items():
        client = MQTTClientWrapper(cfg)
        client.start()
        clients[name] = client

    return clients


mqtt_clients = data_ingestion_by_mqtt(MQTT_SUBSCRIPTION)
