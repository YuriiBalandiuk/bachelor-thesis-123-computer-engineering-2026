from dataclasses import dataclass
from typing import Optional

@dataclass
class MQTTSubscriptionConfig:
    """
    TODO
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