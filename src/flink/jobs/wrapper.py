from pyflink.table import TableEnvironment
from .run_finance_job import FinanceJob


class FlinkJobsWrapper:
    def __init__(
        self,
        t_env: TableEnvironment,
        conn_details: dict,
    ):
        self.finance_job = FinanceJob(job_name="finance_job", t_env=t_env, conn_details=conn_details)
