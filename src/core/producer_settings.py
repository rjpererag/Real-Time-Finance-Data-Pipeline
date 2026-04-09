from .global_vars import global_vars
from ..kafka.producer.settings import KafkaProducerSettings


__CONFIG = {
    "bootstrap.servers": "kafka:9092",
    "client.id": "finance-mocker-v1",
    "acks": "all",
    "compression.type": "snappy",
    "linger.ms": 5,
    "batch.size": 65536,
}

__TOPIC = {
    "topic": global_vars.topic_name,
    "num_partitions": 3,
    "replication_factor": 1,
}


producer_settings = KafkaProducerSettings(
    config=__CONFIG, topic=__TOPIC.get("topic", "my_new_topic"), topic_settings=__TOPIC
)
