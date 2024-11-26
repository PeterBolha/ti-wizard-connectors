from typing import Any

from flask import Request

from config_processors.config_processor import ConfigProcessor


class SatosaConfigProcessor(ConfigProcessor):
    def __init__(self, config):
        super().__init__(config)

    # TODO - implement inspiration in CpclConfigProcessor
    def prepare_configuration(self, request: Request) -> dict[str, Any]:
        pass
