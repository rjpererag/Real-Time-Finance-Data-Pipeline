from .settings import JobSettings
from .flink_job import FlinkJob
from pyflink.table import Table


SINK_SCHEMA = """
            CREATE TABLE btc_moving_avg (
                window_start    TIMESTAMP(3),
                window_end      TIMESTAMP(3),
                ticker          STRING,
                avg_price       DOUBLE,
                ticks           BIGINT
            ) """

SINK_CONN_DETAILS = {
    "connector": "jdbc",
    "url": "jdbc:postgresql://postgres:5432/finance_db",
    "table-name": "btc_moving_avg",
    "username": "admin",
    "password": "admin",
    "sink.buffer-flush.max-rows": "10",
    "sink.buffer-flush.interval": "5s",
}


class FinanceJob(FlinkJob):
    def _get_moving_avg(self, query: str) -> Table | None:
        if query:
            moving_avg = self.t_env.sql_query(query)
            return moving_avg
        return None

    def _sink_moving_avg_to_postgres(self, job_settings: JobSettings) -> None:
        self._logger.info("Sinking data to PostgreSQL")
        insert_sql = f"""
               INSERT INTO btc_moving_avg
               SELECT
                   window_start,
                   window_end,
                   ticker,
                   AVG(price)  AS avg_price,
                   COUNT(*)    AS ticks
               FROM TABLE(
                   TUMBLE(TABLE {job_settings.table_name}, DESCRIPTOR(proc_time), INTERVAL '5' SECONDS)
               )
               GROUP BY window_start, window_end, ticker
           """
        statement_set = self.t_env.create_statement_set()
        statement_set.add_insert_sql(insert_sql)
        job_client = statement_set.execute().get_job_client()

        self._logger.info(f"Flink job submitted: {job_client.get_job_id()}")

    def run_finance_job(
        self,
        job_settings: JobSettings,
    ):
        self._create_table(schema=job_settings.schema)

        if not job_settings.sink:
            result_table = self._get_moving_avg(query=job_settings.sqls.get("price_moving_avg"))
            if result_table:
                self._print_table(table=result_table)

        else:
            self._create_sink_table(schema=SINK_SCHEMA, conn_details=SINK_CONN_DETAILS)
            self._sink_moving_avg_to_postgres(job_settings=job_settings)

    def start(self, job_settings) -> None:
        self._logger.info(f"Starting {self.job_name}")
        self._start_job(
            job_name=self.job_name,
            job_func=self.run_finance_job,
            job_settings=job_settings,
        )
