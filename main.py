import asyncio
from src.websockets.websockets_wrapper import WebsocketWrapper


async def main() -> None:
    queue = asyncio.Queue(maxsize=1000)
    ws = WebsocketWrapper().binance(symbol="btcusdt", queue=queue, print_data=True)
    await ws.connect()


if __name__ == "__main__":
    asyncio.run(main())
