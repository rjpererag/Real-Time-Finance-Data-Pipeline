from .settings import KafkaProducerSettings

import json
import logging
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, settings: KafkaProducerSettings):
        self.settings = settings
        self.producer = self._get_producer()
        self.admin_client = AdminClient({"bootstrap.servers": self.settings.config.get("bootstrap.servers")})

        self.check_topic()

    def create_topic(self) -> None:
        try:
            logger.info(f"Topic {self.settings.topic} not found. Creating topic")
            new_topic = NewTopic(**self.settings.topic_settings)
            self.admin_client.create_topics([new_topic])
            logger.info(f"Topic {self.settings.topic} created")

        except Exception as e:
            logger.error(f"Failed to create topic {self.settings.topic}: {str(e)}")

    def check_topic(self) -> None:
        metadata = self.admin_client.list_topics(timeout=10)
        if self.settings.topic not in metadata.topics:
            self.create_topic()

    def _get_producer(self) -> Producer | None:
        try:
            logger.info("Getting producer")
            return Producer(self.settings.config)
        except Exception as e:
            logger.error(f"Failed to get Kafka Producer: {str(e)}")
            return None

    @staticmethod
    def _delivery_report(err, msg):
        if err is not None:
            logger.error(f"Message lost! Error: {err}. {msg}")
        else:
            logger.info("Message sent")

    def _produce_msg(self, data: dict, tag: str) -> None:
        try:
            self.producer.produce(
                topic=self.settings.topic,
                key=tag,
                value=json.dumps(data).encode("utf-8"),
                callback=self._delivery_report,
            )
            self.producer.poll(0)

        except BufferError:
            logger.error("Producer buffer overflow, waiting...")
            self.producer.flush(1)

        except Exception as e:
            logger.error(f"Failed to produce message: {str(e)}")

    def produce(
        self,
        data: dict,
        tag: str,
    ) -> None:
        if not self.producer:
            logger.warning("Kafka Producer not initialized")
            return

        self._produce_msg(data=data, tag=tag)

    def close(self) -> None:
        logger.info("Closing Kafka Producer")
        self.producer.flush()
