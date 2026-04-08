from ..settings import JobSettings
from .flink_job import FlinkJob
from pyflink.table import Table


class FinanceJob(FlinkJob):
    def _get_moving_avg(self, query: str) -> Table | None:
        if query:
            moving_avg = self.t_env.sql_query(query)
            return moving_avg
        return None

    def run_finance_job(
        self,
        job_settings: JobSettings,
    ):
        self._create_table(schema=job_settings.schema)
        result_table = self._get_moving_avg(query=job_settings.sqls.get("price_moving_avg"))
        if result_table:
            self._print_table(table=result_table)

    def start(self, job_settings) -> None:
        self._logger.info(f"Starting {self.job_name}")
        self._start_job(
            job_name=self.job_name,
            job_func=self.run_finance_job,
            job_settings=job_settings,
        )
