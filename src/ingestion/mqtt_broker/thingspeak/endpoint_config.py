import os
from typing import Dict
from dotenv import load_dotenv

from src.ingestion.config.config_models import MQTTSubscriptionConfig

load_dotenv(".env")

def build_topics(*env_keys: str) -> list[str]:
    """
    TODO
    """
    return [
        f"channels/{os.getenv(key)}/subscribe"
        for key in env_keys
            if os.getenv(key)
    ]


MQTT_SUBSCRIPTION: Dict[str, MQTTSubscriptionConfig] = {
    "channels_thingspeak": MQTTSubscriptionConfig(
        broker="mqtt3.thingspeak.com",
        port=1883,
        client_id=os.getenv("CLIENT_ID"),
        client_username=os.getenv("MQTT_USERNAME"),
        client_password=os.getenv("MQTT_PASSWORD"),
        topic=build_topics("CHANNEL_ID_1", "CHANNEL_ID_2"),
        qos=0,
        clean_session=True,
    )
}
