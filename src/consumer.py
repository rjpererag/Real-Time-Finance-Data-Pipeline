from src.flink import FlinkService, FlinkJobs
from src.core.consumer_settings import flink_settings, job_settings


def main() -> None:
    service = FlinkService(settings=flink_settings)
    jobs = FlinkJobs(t_env=service.t_env, conn_details=service.settings.connection)
    jobs.finance_job.start(job_settings=job_settings.get("finance_job"))


if __name__ == "__main__":
    main()
