from dataclasses import field, dataclass
from typing import Optional

DEFAULT_CONN = {
    "connector": "kafka",
    "topic": "my_new_topic",
    "properties.bootstrap.servers": "kafka:29092",
    "properties.group.id": "flink-finance-group",
    "scan.startup.mode": "earliest-offset",
    "format": "json",
}


def get_default_sql_schema(
    table_name: str,
    watermark: str | int,
) -> str:
    return f"""CREATE TABLE {table_name} (
        ticker STRING,
        price DOUBLE,
        `timestamp` TIMESTAMP(3),
        WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '{watermark}' SECOND
    )"""


@dataclass
class JobSettings:
    table_name: str = "kafka_raw_market"
    watermark: int = 5
    schema: Optional[str] = field(default=None, init=True)

    def __post_init__(self):
        if self.schema is None:
            self.schema = get_default_sql_schema(table_name=self.table_name, watermark=self.watermark)


@dataclass
class FlinkSettings:
    connection: dict = field(default_factory=lambda: DEFAULT_CONN)
