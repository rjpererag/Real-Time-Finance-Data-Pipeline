from src.kafka import KafkaBuffer
from data_generator import DataGenerator
from time import sleep

from src.core import producer_settings


GENERATOR = DataGenerator()
PRODUCER = KafkaBuffer(
    producer_settings=producer_settings,
).get_producer()


def main() -> None:
    try:
        while True:
            data = GENERATOR.financial.generate(ticker="btc.eur")
            PRODUCER.produce(
                data=data,
                tag=data.get("ticker"),
            )
            sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        print("Finalizing transit...")
        PRODUCER.close()


if __name__ == "__main__":
    main()
