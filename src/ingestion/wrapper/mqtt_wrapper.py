import re
import logging
import paho.mqtt.client as mqtt

from src.ingestion.config.config_models import MQTTSubscriptionConfig

# logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s - {%(name)s} - %(message)s:"
)


class MQTTClientWrapper:

    def __init__(self, config: MQTTSubscriptionConfig):
        """
        TODO
        """
        self.config = config
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=config.client_id,
            clean_session=config.clean_session,
        )
        self.client.enable_logger()

        if self.config.client_username and self.config.client_password:
            self.client.username_pw_set(config.client_username, config.client_password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message


    def on_connect(self, client, userdata, flags, reason_code, properties):
        """
        TODO
        """
        logging.info(f"Connected with result code - {reason_code}")
        self.client.subscribe([(t, self.config.qos) for t in self.config.topic])


    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        """
        TODO
        """
        print(f"Disconnected with result code {reason_code}")


    def on_message(self, client, userdata, msg):
        """
        TODO
        """
        match = re.search(r"channels/(\d+)/subscribe", msg.topic)
        if not match:
            logging.error(f"No subscribed channel configured")

        channel_id = match.group(1)
        logging.info(f"Received message from {channel_id}: {msg.payload.decode()}")


    def start(self):
        """
        TODO
        """
        self.client.connect(self.config.broker, self.config.port)
        self.client.loop_forever()
        # self.client.loop_start()


    def stop(self):
        """
        TODO
        """
        self.client.loop_stop()
        self.client.disconnect()
