from .global_vars import global_vars
from ..flink import FlinkSettings, JobSettings


# SERVICE SETTINGS -------------------------------------------------------
__FLINK_CLUSTER_CONN = {
    "connector": "kafka",
    "topic": global_vars.topic_name,
    "properties.bootstrap.servers": global_vars.kafka_bootstrap_server,
    "properties.group.id": global_vars.kafka_group_id,
    "scan.startup.mode": "earliest-offset",
    "format": "json",
}

flink_settings = FlinkSettings(connection=__FLINK_CLUSTER_CONN)


# JOB SETTINGS -----------------------------------------------------------
# FINANCE JOB SETTINGS
def __get_pricing_schema(
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


def __get_price_moving_avg_sql(
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


def __get_price_moving_avg_sink_sql(
    table_name: str,
    sink_table_name: str,
    event_mode: str,
) -> dict:
    sink_schema = f"""
                CREATE TABLE {sink_table_name} (
                    window_start    TIMESTAMP(3),
                    window_end      TIMESTAMP(3),
                    ticker          STRING,
                    avg_price       DOUBLE,
                    ticks           BIGINT
                )
                """

    sink_conn_details = {
        "connector": "jdbc",
        "url": global_vars.postgres_url,
        "table-name": sink_table_name,
        "username": global_vars.postgres_user,
        "password": global_vars.postgres_password,
        "sink.buffer-flush.max-rows": "10",
        "sink.buffer-flush.interval": "5s",
    }

    insert_sql = f"""
           INSERT INTO {sink_table_name}
           SELECT
               window_start,
               window_end,
               ticker,
               AVG(price)  AS avg_price,
               COUNT(*)    AS ticks
           FROM TABLE(
               TUMBLE(TABLE {table_name}, DESCRIPTOR({event_mode}), INTERVAL '5' SECONDS)
           )
           GROUP BY window_start, window_end, ticker
       """

    return {
        "sink_price_moving_avg": {
            "sink_schema": sink_schema,
            "sink_conn_details": sink_conn_details,
            "insert_sql": insert_sql,
        }
    }


def __get_run_finance_job_settings(
    table_name: str = "kafka_raw_market",
    sink_table_name: str = "btc_moving_avg",
    watermark: int = 5,
    event_mode: str = "proc_time",
    sink: bool = False,
) -> JobSettings:
    schema = __get_pricing_schema(table_name=table_name, watermark=watermark)
    sqls = {
        **__get_price_moving_avg_sql(table_name=table_name, event_mode=event_mode),
        **__get_price_moving_avg_sink_sql(
            table_name=table_name, sink_table_name=sink_table_name, event_mode=event_mode
        ),
    }

    return JobSettings(
        table_name=table_name,
        watermark=watermark,
        event_mode=event_mode,
        schema=schema,
        sqls=sqls,
        sink=sink,
    )


job_settings = {
    "finance_job": __get_run_finance_job_settings(
        watermark=1,
        sink=True,
    )
}
