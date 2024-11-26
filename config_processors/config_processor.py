from abc import ABC, abstractmethod
from typing import Any

from flask import Request

from config_version_managers.config_version_manager_initializer import \
    ConfigVersionManagerInitializer


class ConfigProcessor(ABC):
    def __init__(self, config):
        self.observed_entity_filters = config.get("filters")
        config_version_manager_cfg = config.get("version_manager", {})
        config_version_manager_initializer = ConfigVersionManagerInitializer(
            config_version_manager_cfg
        )
        self.__CONFIG_VERSION_MANAGER = (
            config_version_manager_initializer.get_config_version_manager()
        )

    def save_configuration(self, config: dict[str, Any]) -> None:
        self.__CONFIG_VERSION_MANAGER.save_configuration(config)

    @abstractmethod
    def prepare_configuration(self, request: Request) -> dict[str, Any]:
        pass

    def update_configuration(self, request: Request) -> None:
        config = self.prepare_configuration(request)
        self.save_configuration(config)
