from src.kafka import KafkaBuffer
from src.data_generator import DataGenerator
from time import sleep

from src.core.producer_settings import producer_settings


def main() -> None:
    GENERATOR = DataGenerator()
    PRODUCER = KafkaBuffer(
        producer_settings=producer_settings,
    ).get_producer()

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
