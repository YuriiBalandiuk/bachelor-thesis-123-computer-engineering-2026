from dataclasses import dataclass
from typing import Optional

@dataclass
class MQTTSubscriptionConfig:
    """
    TODO
    """
    broker: str
    port: int
    client_username: str
    client_password: str
    client_id: str
    topic: list[str]
    qos: Optional[int] = None
    clean_session: Optional[bool] = None