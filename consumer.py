from src.flink import FlinkService, FlinkSettings, FlinkJobs, JobSettings


def main() -> None:
    settings = FlinkSettings()
    job_settings = JobSettings(
        watermark=1,
        sink=True,
    )

    service = FlinkService(settings=settings)
    jobs = FlinkJobs(t_env=service.t_env, conn_details=service.settings.connection)
    jobs.finance_job.start(job_settings=job_settings)


if __name__ == "__main__":
    main()
