from .abstract import AbstractDataGenerator

import random
from datetime import datetime
from functools import reduce


class FinancialDataGenerator(AbstractDataGenerator):
    def __init__(self):
        self.__options = self.__get_tickets_options()

    @staticmethod
    def __get_tickets_options() -> dict:
        return {
            "btc": {
                "usdt": {
                    "ticker": "BTCUSDT",
                    "base_price": 50000,
                },
                "eur": {
                    "ticker": "BTCEUR",
                    "base_price": 50000,
                },
            }
        }

    @staticmethod
    def deep_get(
        data: dict,
        path: str,
        default: dict | None = None,
    ):
        """
        Retrieves a value from a nested dictionary using a dot-separated path.
        """
        try:
            return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, path.split("."), data)
        except (AttributeError, TypeError):
            return default

    def _get_random_data(self) -> dict:
        options = []
        for key, value in self.__options.items():
            opts = [f"{key}.{val_key}" for val_key in list(value.keys())]
            options.extend(opts)

        random_ticker = random.choice(options)
        return self._get_from_option(ticker=random_ticker)

    def _get_from_option(self, ticker: str) -> dict:
        base_data = self.deep_get(
            data=self.__options,
            path=ticker,
        )

        return base_data

    def _get_base_data(
        self,
        ticker: str,
        choose_random: bool,
    ) -> dict:
        try:
            if not choose_random:
                return self._get_from_option(ticker=ticker)
            return self._get_random_data()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def _get_random_price(base_price: int | float) -> int | float:
        return round((1 + random.random()) * base_price, 2)

    def generate(
        self,
        ticker: str = "btc.usdt",
        choose_random: bool = False,
    ) -> dict:
        base_data = self._get_base_data(ticker, choose_random=choose_random)

        if base_data.get("error"):
            return base_data

        return {
            "ticker": base_data.get("ticker"),
            "price": self._get_random_price(base_price=base_data.get("base_price", 0)),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        }
