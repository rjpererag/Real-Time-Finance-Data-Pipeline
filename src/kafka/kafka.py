from .consumer.service import KafkaConsumer
from .consumer.settings import KafkaConsumerSettings
from .producer.service import KafkaProducer
from .producer.settings import KafkaProducerSettings


class KafkaBuffer:
    def __init__(
        self,
        consumer_settings: KafkaConsumerSettings = KafkaConsumerSettings(),
        producer_settings: KafkaProducerSettings = KafkaProducerSettings(),
    ):
        self.consumer_settings = consumer_settings
        self.producer_settings = producer_settings

    def get_producer(self) -> KafkaProducer | None:
        return KafkaProducer(settings=self.producer_settings)

    def get_consumer(self) -> KafkaConsumer | None:
        return KafkaConsumer(settings=self.consumer_settings)
