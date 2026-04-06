from .settings import KafkaConsumerSettings


class KafkaConsumer:
    def __init__(self, settings: KafkaConsumerSettings):
        self.settings = settings

    def start(self) -> None:
        pass
