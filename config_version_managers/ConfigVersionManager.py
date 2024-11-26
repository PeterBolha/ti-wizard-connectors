from abc import ABC, abstractmethod
from typing import Any


class ConfigVersionManager(ABC):
    @abstractmethod
    def save_configuration(self, config: dict[str, Any]) -> None:
        pass
