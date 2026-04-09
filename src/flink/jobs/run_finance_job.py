from .settings import JobSettings
from .flink_job import FlinkJob
from pyflink.table import Table


class FinanceJob(FlinkJob):
    def _get_moving_avg(self, query: str) -> Table | None:
        if query:
            moving_avg = self.t_env.sql_query(query)
            return moving_avg
        return None

    def _sink_moving_avg_to_postgres(self, insert_sql: str) -> None:
        if not insert_sql:
            self._logger.warning("No insert_sql provided to sink data, skipping ... ")
            return

        self._logger.info("Sinking data to PostgreSQL")
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
            sink_schema = job_settings.sqls.get("sink_price_moving_avg", {}).get("sink_schema")
            sink_conn_details = job_settings.sqls.get("sink_price_moving_avg", {}).get("sink_conn_details")
            sink_insert_sql = job_settings.sqls.get("sink_price_moving_avg", {}).get("insert_sql")

            self._create_sink_table(schema=sink_schema, conn_details=sink_conn_details)
            self._sink_moving_avg_to_postgres(insert_sql=sink_insert_sql)

    def start(self, job_settings) -> None:
        self._logger.info(f"Starting {self.job_name}")
        self._start_job(
            job_name=self.job_name,
            job_func=self.run_finance_job,
            job_settings=job_settings,
        )
