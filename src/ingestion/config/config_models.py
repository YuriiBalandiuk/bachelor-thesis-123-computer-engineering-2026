from dataclasses import dataclass, field
from typing import Optional, Literal, Dict, Any, List

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