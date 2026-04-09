from dataclasses import dataclass, field
from typing import Optional


def get_default_sql_schema(
    table_name: str,
    watermark: str | int,
) -> str:
    return f"""CREATE TABLE {table_name} (
        ticker STRING,
        price DOUBLE,
        `timestamp` TIMESTAMP(3),
        proc_time AS PROCTIME(),
        WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '{watermark}' SECOND
    )"""


def get_default_sqls(
    table_name: str,
    event_mode: str,
) -> dict:
    price_moving_avg = f"""
        SELECT
            window_start,
            window_end,
            ticker,
            AVG(price) AS avg_price,
            COUNT(*) AS ticks
        FROM TABLE(
            TUMBLE(TABLE {table_name}, DESCRIPTOR({event_mode}), INTERVAL '5' SECONDS)
        )
        GROUP BY window_start, window_end, ticker
    """

    return {"price_moving_avg": price_moving_avg}


@dataclass
class JobSettings:
    table_name: str = "kafka_raw_market"
    watermark: int = 5
    event_mode: str = "proc_time"
    schema: Optional[str] = field(default=None, init=True)
    sqls: Optional[dict] = field(default=None, init=True)
    sink: bool = False

    def __post_init__(self):
        if self.schema is None:
            self.schema = get_default_sql_schema(table_name=self.table_name, watermark=self.watermark)

        if self.sqls is None:
            self.sqls = get_default_sqls(table_name=self.table_name, event_mode=self.event_mode)
