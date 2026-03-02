from dataclasses import dataclass
from typing import Optional

@dataclass
class MQTTSubscriptionConfig:
    """
    Configuration container for MQTT-to-Kafka subscription pipeline.

    This data structure encapsulates connection parameters for an MQTT
    broker along with target Kafka routing configuration. It represents
    a fully resolved, runtime-ready configuration object.

    Attributes:
        kafka_bootstrap: Kafka bootstrap server address in the form
            "host:port" or comma-separated list for clusters.
        kafka_topic: Target Kafka topic where incoming MQTT messages
            will be published.
        broker: Hostname or IP address of the MQTT broker.
        port: Network port of the MQTT broker.
        client_username: Username used for MQTT authentication.
        client_password: Password used for MQTT authentication.
        client_id: Unique MQTT client identifier.
        topic: List of MQTT topics to subscribe to.
        qos: Optional MQTT Quality of Service level (0, 1, or 2).
        clean_session: Optional flag indicating whether to use a clean
            session when establishing the MQTT connection.

    Notes:
        - 'qos' must comply with MQTT specification values (0, 1, 2).
        - 'client_id' must be unique per broker session.
        - 'topic' entries must be valid MQTT topic filters.
    """
    kafka_bootstrap: str
    kafka_topic: str
    broker: str
    port: int
    client_username: str
    client_password: str
    client_id: str
    topic: list[str]
    qos: Optional[int] = None
    clean_session: Optional[bool] = None