from typing import Dict

from src.ingestion.config.config_models import MQTTSubscriptionConfig
from src.common.env_config import EnvConfig

env_config = EnvConfig(env_path=".env",
    required_keys=["CLIENT_ID", "MQTT_USERNAME", "MQTT_PASSWORD", "CHANNEL_IDS"]
)


MQTT_SUBSCRIPTION: Dict[str, MQTTSubscriptionConfig] = {
    "channels_thingspeak": MQTTSubscriptionConfig(
        kafka_bootstrap="kafka1:9092,kafka2:9092",
        kafka_topic="thingspeak-topic",
        broker="mqtt3.thingspeak.com",
        port=1883,
        client_id=env_config.client_id,
        client_username=env_config.mqtt_username,
        client_password=env_config.mqtt_password,
        topic=env_config.mqtt_channels,
        qos=0,
        clean_session=True,
    )
}
