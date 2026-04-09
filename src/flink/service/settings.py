from dataclasses import field, dataclass

DEFAULT_CONN = {
    "connector": "kafka",
    "topic": "my_new_topic",
    "properties.bootstrap.servers": "kafka:29092",
    "properties.group.id": "flink-finance-group",
    "scan.startup.mode": "earliest-offset",
    "format": "json",
}


@dataclass
class FlinkSettings:
    connection: dict = field(default_factory=lambda: DEFAULT_CONN)
