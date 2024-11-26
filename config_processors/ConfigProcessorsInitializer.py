from typing import List

from config_processors.ConfigProcessor import ConfigProcessor
from config_processors.CpclConfigProcessor import CpclConfigProcessor
from config_processors.SatosaConfigProcessor import SatosaConfigProcessor
from enums.ConfigProcessorType import ConfigProcessorType


class ConfigProcessorsInitializer:
    def __init__(self, processors_cfg):
        self.__PROCESSORS_CFG = processors_cfg

    def get_processors(self) -> List[ConfigProcessor]:
        shared_settings = self.__PROCESSORS_CFG.get("shared_settings", {})
        processor_specific_settings = self.__PROCESSORS_CFG.get(
            "processor_specific_settings", {}
        )

        configured_processors = []
        for cfg_values in processor_specific_settings.values():
            try:
                processor_type_in_cfg = cfg_values.get("type")
                processor_type = ConfigProcessorType[processor_type_in_cfg]
            except KeyError:
                raise ValueError(
                    f"Invalid config processor type '{processor_type_in_cfg}' in configuration. "
                    f"Allowed values are: {', '.join([e.name for e in ConfigProcessorType])}"
                )

            processor_specific_config = {**shared_settings, **cfg_values}
            match processor_type:
                case ConfigProcessorType.CPCL:
                    configured_processors.append(
                        CpclConfigProcessor(processor_specific_config)
                    )
                case ConfigProcessorType.SATOSA:
                    configured_processors.append(
                        SatosaConfigProcessor(processor_specific_config)
                    )

        return configured_processors
