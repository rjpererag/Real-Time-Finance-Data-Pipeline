from dataclasses import dataclass, field


BASE_CONFIG = {
    "bootstrap.servers": "localhost:9092",
    "client.id": "finance-mocker-v1",
    "acks": "all",
    "compression.type": "snappy",
    "linger.ms": 5,
    "batch.size": 65536,
}

BASE_TOPIC = {
    "topic": "my_new_topic",
    "num_partitions": 3,
    "replication_factor": 1,
}


@dataclass
class KafkaProducerSettings:
    config: dict = field(default_factory=lambda: BASE_CONFIG)
    topic: str = BASE_TOPIC.get("topic")
    topic_settings: dict = field(default_factory=lambda: BASE_TOPIC)
