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
        self.consumer = KafkaConsumer(settings=consumer_settings)
        self.producer = KafkaProducer(settings=producer_settings)
