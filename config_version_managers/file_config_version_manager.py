import json
from abc import abstractmethod
from typing import Any, Dict

import yaml

from config_version_managers.config_version_manager import ConfigVersionManager
from enums.config_file_format import ConfigFileFormat


class FileConfigVersionManager(ConfigVersionManager):
    def __init__(self, file_version_manager_cfg):
        self._CONFIG_FILE_NAME = file_version_manager_cfg.get(
            "config_file_name"
        )

        try:
            config_file_format_in_cfg = file_version_manager_cfg.get(
                "config_file_format"
            )
            config_file_format = ConfigFileFormat[config_file_format_in_cfg]
        except KeyError:
            raise ValueError(
                f"Invalid config file format '{config_file_format_in_cfg}' in "
                f"configuration. "
                f"Allowed values are: "
                f"{', '.join([e.name for e in ConfigFileFormat])}"
            )

        self._CONFIG_FILE_FORMAT = config_file_format

    def save_config_txt(self, config, file_path: str) -> str:
        file_path += ".txt"
        with open(file_path, "w") as txt_file:
            txt_file.write(str(config))
        return file_path

    def save_config_json(self, config, file_path: str) -> str:
        file_path += ".json"
        with open(file_path, "w") as json_file:
            json.dump(config, json_file, indent=4)
        return file_path

    def save_config_yaml(self, config, file_path: str) -> str:
        file_path += ".yaml"
        with open(file_path, "w") as yaml_file:
            yaml.dump(
                config, yaml_file, default_flow_style=False, sort_keys=False
            )
        return file_path

    def save_config_to_file(
        self,
        file_path: str,
        config: Dict[str, Any],
        output_format: ConfigFileFormat = None,
    ) -> str:
        if not output_format:
            output_format = self._CONFIG_FILE_FORMAT

        match output_format:
            case output_format.TXT:
                return self.save_config_txt(config, file_path)
            case output_format.JSON:
                return self.save_config_json(config, file_path)
            case output_format.YAML:
                return self.save_config_yaml(config, file_path)

    @abstractmethod
    def save_configuration(self, config: dict[str, Any]) -> None:
        pass
