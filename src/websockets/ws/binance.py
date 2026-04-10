from .ws import Websocket
from ..dataclasses.binance import Stream
import json


class BinanceWebsocket(Websocket):
    def __init__(self, symbol: str, stream: str = "aggTrade", base_url="wss://stream.binance.com:9443"):
        self.base_url = base_url
        url = self._get_url(symbol=symbol, stream=stream)
        super().__init__(url=url)

    def _get_url(self, symbol: str, stream: str) -> str:
        stream = f"{symbol.lower()}@{stream}"
        return f"{self.base_url}/ws/{stream}"

    async def on_message(self, message) -> Stream | None:
        self._logger.debug(f"Received message: {message}")
        data = json.loads(message)
        parsed_data = await self._handle_data(data=data)
        print(parsed_data)

    async def _handle_data(self, data: dict) -> Stream | None:
        if not data:
            return None
        try:
            return self._parse(data=data)
        except Exception as e:
            self._logger.error(f"Error parsing: {str(e)}")

    @staticmethod
    def _parse(data: dict) -> Stream:
        return Stream(**data)
