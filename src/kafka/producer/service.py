from .settings import KafkaProducerSettings


class KafkaProducer:
    def __init__(self, settings: KafkaProducerSettings):
        self.settings = settings

    def start(self) -> None:
        pass
