import asyncio

from .ws import Websocket
from ..dataclasses.binance import Stream
import json


class BinanceWebsocket(Websocket):
    def __init__(
        self,
        queue: asyncio.Queue,
        symbol: str,
        stream: str = "aggTrade",
        base_url="wss://stream.binance.com:9443",
        print_data: bool = False,
    ):
        self.queue = queue
        self.base_url = base_url
        self.print = print_data
        url = self._get_url(symbol=symbol, stream=stream)
        super().__init__(url=url)

    def _get_url(self, symbol: str, stream: str) -> str:
        stream = f"{symbol.lower()}@{stream}"
        return f"{self.base_url}/ws/{stream}"

    async def on_message(self, message) -> None:
        self._logger.debug(f"Received message: {message}")
        data = json.loads(message)
        await self._handle_data(data=data)

    async def _handle_data(self, data: dict) -> None:
        if not data:
            return None
        try:
            parsed_data = self._parse(data=data)
            if self.print:
                print(parsed_data)
            await self.queue.put(parsed_data)

        except Exception as e:
            self._logger.error(f"Error parsing: {str(e)}")

    @staticmethod
    def _parse(data: dict) -> Stream:
        return Stream(**data)
