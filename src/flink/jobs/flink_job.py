from .abstract import AbstractFlinkJob
from .utils import parse_connection_details_to_str
from pyflink.table import TableEnvironment, Table
from typing import Callable
import logging
from logging import Logger


class FlinkJob(AbstractFlinkJob):
    def __init__(
        self,
        job_name: str,
        t_env: TableEnvironment,
        conn_details: dict,
    ):
        super().__init__()
        self.t_env = t_env
        self.conn_details = conn_details
        self._logger = self.__get_logger()

        self.job_name: str = job_name
        self.job_func: Callable | None = None

    @staticmethod
    def __get_logger() -> Logger:
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def _start_job(self, job_name: str, job_func: Callable, *args, **kwargs) -> None:
        try:
            job_func(*args, **kwargs)
        except Exception as e:
            self._logger.error(f"Failed {job_name}: {str(e)}")

    def _create_table(self, schema: str):
        parsed_conn = parse_connection_details_to_str(self.conn_details)
        full_sql = f"{schema} WITH ({parsed_conn})"
        self.t_env.execute_sql(full_sql)

    @staticmethod
    def _print_table(table: Table) -> None:
        table.execute().print()

    def start(self, *args, **kwargs) -> None:
        pass
