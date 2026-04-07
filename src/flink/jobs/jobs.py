from .run_finance_job import run_finance_job


class FlinkJobs:
    def __init__(self):
        self.run_finance_job = run_finance_job
