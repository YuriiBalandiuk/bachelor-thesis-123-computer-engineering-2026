import re
import logging
import paho.mqtt.client as mqtt
from confluent_kafka import Producer

from src.ingestion.config.config_models import MQTTSubscriptionConfig

logger = logging.getLogger(__name__)


class MQTTClientWrapper:
    """
    Wrapper for MQTT client to consume messages and forward them to Kafka.

    Encapsulates an MQTT client configured via 'MQTTSubscriptionConfig',
    subscribes to specified topics, and produces messages to a Kafka
    topic. Handles connection, disconnection, message reception, and
    error reporting.

    Attributes:
        config: MQTT subscription and Kafka configuration.
        client: Initialized paho-mqtt client with callbacks.
        producer: Kafka producer instance for publishing messages.
    """

    def __init__(self, 
        config: MQTTSubscriptionConfig
    ) -> None:
        """
        Initialize MQTT client and Kafka producer.

        Sets up MQTT callbacks (connect, disconnect, message) and
        credentials if provided.

        Args:
            config: 'MQTTSubscriptionConfig' object with MQTT broker,
                topics, and Kafka target settings.
        """
        self.config = config

        try:
            self.client = mqtt.Client(
                mqtt.CallbackAPIVersion.VERSION2,
                client_id=config.client_id,
                clean_session=config.clean_session,
            )

            self.client.enable_logger()
        except Exception as e:
            logging.error(f"Client object has not been created - {e}")

        if self.config.client_username and self.config.client_password:
            self.client.username_pw_set(config.client_username, config.client_password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        try:
            self.producer = Producer({'bootstrap.servers': config.kafka_bootstrap})
        except Exception as e:
                logging.error(f"Producer object has not been created - {e}")

    def on_connect(self, 
        client, 
        userdata, 
        flags, 
        reason_code, 
        properties
    ) -> None:
        """
        Callback executed when the MQTT client connects to the broker.

        Subscribes to all configured MQTT topics upon successful
        connection.

        Args:
            client: MQTT client instance.
            userdata: User-defined data.
            flags: Connection flags.
            reason_code: Connection result code.
            properties: MQTT v5 connection properties.
        """
        logging.info(f"Connected with result code - {reason_code}")
        self.client.subscribe([(t, self.config.qos) for t in self.config.topic])


    def on_disconnect(self, 
        client, 
        userdata, 
        flags, 
        reason_code, 
        properties
    ) -> None:
        """
        Callback executed when the MQTT client disconnects from the broker.

        Args:
            client: MQTT client instance.
            userdata: User-defined data.
            flags: Disconnection flags.
            reason_code: Disconnection result code.
            properties: MQTT v5 properties.
        """
        print(f"Disconnected with result code {reason_code}")


    def on_message(self, 
        client, 
        userdata, 
        msg
    ) -> None:
        """
        Callback executed when a subscribed MQTT message is received.

        Extracts channel ID from the topic, logs message, and forwards
        the payload to the configured Kafka topic. Handles buffer and
        produce errors gracefully.

        Args:
            client: MQTT client instance.
            userdata: User-defined data.
            msg: MQTT message object containing topic and payload.
        """
        try:
            logging.info(f"Checking broker availability...")
            self.producer.list_topics(timeout=10)
            logging.info(f"Checking broker availability - Success")
            
            match = re.search(r"channels/(\d+)/subscribe", msg.topic)
            if not match:
                logging.error(f"No subscribed channel configured")
                return

            channel_id = match.group(1)
            logging.info(f"Received message from {channel_id}: {msg.payload.decode()}")

            self.producer.produce(
                topic=self.config.kafka_topic,
                key=channel_id.encode(),
                value=msg.payload,
            )

            logging.info(f"Sending to Kafka topic - {self.config.kafka_topic}")
            self.producer.poll(0)
            logging.info(f"Sent data to Kafka topic - Success")
        except BufferError as e:
            logging.error(f"Kafka buffer full - {e}")
            self.stop()
        except Exception as e:
            logging.error(f"Kafka produce error - {e}")


    def start(self) -> None:
        """
        Start MQTT client loop and begin consuming messages.

        Connects to the MQTT broker using configured host and port,
        then enters a blocking loop to receive messages continuously.
        """
        logger.info("Starting data fetch from Thingspeak MQTT clients")

        self.client.connect(self.config.broker, self.config.port)
        self.client.loop_forever()
        # self.client.loop_start()


    def stop(self) -> None:
        """
        Stop MQTT client loop and flush pending Kafka messages.

        Disconnects the MQTT client, stops the network loop, and
        flushes any remaining messages in the Kafka producer buffer.
        """
        logger.info("Stopping data fetch from Thingspeak MQTT clients")

        self.client.loop_stop()
        self.client.disconnect()
        self.producer.flush()
