from abc import ABC, abstractmethod
from typing import Any


class AbstractDataGenerator(ABC):
    @abstractmethod
    def generate(self, *args, **kwargs) -> Any:
        ...
