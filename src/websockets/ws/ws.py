import asyncio
import logging
import websockets
from websockets.exceptions import ConnectionClosed
from tenacity import (
    AsyncRetrying,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    # before_sleep_log
)


class Websocket:
    def __init__(self, url: str):
        self.url = url
        self._logger: logging.Logger = self.__get_logger()
        self._stop = False

        self.wait_exponential = {"multiplier": 1, "min": 2, "max": 60}
        self.stop_after_attempt = 9999
        self.retry_if_exception_type = (ConnectionClosed, OSError)

    @staticmethod
    def __get_logger() -> logging.Logger:
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def _get_retrier(self) -> AsyncRetrying:
        return AsyncRetrying(
            wait=wait_exponential(**self.wait_exponential),
            stop=stop_after_attempt(self.stop_after_attempt),
            retry=retry_if_exception_type(self.retry_if_exception_type),
            # before_sleep=before_sleep_log(self._logger, logging.INFO),
            retry_error_callback=lambda _: self._logger.info("Retry stopped by user."),
        )

    async def _listen(self, ws) -> None:
        self._logger.info("Listening to WSS")
        async for message in ws:
            if self._stop:
                break
            await self.on_message(message)

    async def _run_connection(self):
        async with websockets.connect(self.url) as ws:
            self._logger.info(f"Connected to {self.url}")
            await self._listen(ws)

    async def connect(self):
        while not self._stop:
            retrier = self._get_retrier()
            try:
                self._logger.info(f"Connecting to WSS: {self.url}")
                await retrier(self._run_connection)

            except Exception as e:
                self._logger.error(f"Connection lost: {str(e)}. Retrying in 5 seconds...")
                await asyncio.sleep(5)

    async def on_message(self, message) -> None:
        raise NotImplementedError("Child classes must implement on_message")

    def stop(self):
        self._stop = True
