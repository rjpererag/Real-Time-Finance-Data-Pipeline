from .settings import FlinkSettings

from pyflink.table import EnvironmentSettings, TableEnvironment
import logging
from logging import Logger


class FlinkService:
    def __init__(self, settings: FlinkSettings):
        self.__active = False
        self.__logger = self.__get_logger()
        self.settings = settings

        self.t_env = self.get_table_env()

    @staticmethod
    def __get_logger() -> Logger:
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def get_table_env(
        self,
    ) -> TableEnvironment | None:
        try:
            settings = EnvironmentSettings.in_streaming_mode()
            t_env = TableEnvironment.create(settings)
            self.__active = True
            return t_env

        except Exception as e:
            self.__logger.error(f"Error while getting table env: {e}")
            self.__active = False
            return None
