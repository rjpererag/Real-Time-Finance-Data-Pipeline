from src.flink.settings import FlinkSettings, JobSettings

from src.flink import FlinkService
from src.flink.jobs.wrapper import FlinkJobsWrapper


def main() -> None:
    settings = FlinkSettings()
    job_settings = JobSettings(
        watermark=1,
    )

    service = FlinkService(settings=settings)
    jobs = FlinkJobsWrapper(t_env=service.t_env, conn_details=service.settings.connection)

    jobs.finance_job.start(job_settings=job_settings)


if __name__ == "__main__":
    main()
