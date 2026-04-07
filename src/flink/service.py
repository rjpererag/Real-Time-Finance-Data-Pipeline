from .jobs.jobs import FlinkJobs
from .settings import FlinkSettings

from pyflink.table import EnvironmentSettings, TableEnvironment


class FlinkService:
    def __init__(self, settings: FlinkSettings):
        self._settings = settings
        self.jobs = FlinkJobs()
        self.t_env = self.get_table_env()

    @staticmethod
    def get_table_env() -> TableEnvironment:
        settings = EnvironmentSettings.in_streaming_mode()
        t_env = TableEnvironment.create(settings)
        return t_env
