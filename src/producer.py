import asyncio

from src.kafka.producer.service import KafkaProducer
from src.websockets.websockets_wrapper import WebsocketWrapper
from src.websockets.dataclasses.binance import Stream
from src.kafka import KafkaBuffer

from src.core.producer_settings import producer_settings


async def kafka_worker(queue: asyncio.Queue, producer: KafkaProducer):
    while True:
        data: Stream
        data = await queue.get()

        try:
            payload = {"ticker": data.symbol, "price": data.price, "timestamp": data.event_time} if data else None

            producer.produce(
                data=payload,
                tag=data.symbol,
            )
        except Exception as e:
            print(str(e))
        finally:
            queue.task_done()


async def main():
    kafka_producer = KafkaBuffer(
        producer_settings=producer_settings,
    ).get_producer()

    queue = asyncio.Queue(maxsize=1000)
    binance_ws = WebsocketWrapper().binance(queue=queue, symbol="btcusdt")

    try:
        await asyncio.gather(binance_ws.connect(), kafka_worker(queue, kafka_producer))

    except Exception as e:
        print(f"Main loop error: {e}")

    finally:
        print("Finalizing transit...")
        kafka_producer.close()


if __name__ == "__main__":
    asyncio.run(main())
