import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from config_version_managers.config_version_manager import ConfigVersionManager
from enums.config_file_format import ConfigFileFormat


class LocalConfigVersionManager(ConfigVersionManager):
    def __init__(self, local_version_manager_cfg):
        self.__CONFIG_FOLDER_PATH = Path(
            local_version_manager_cfg.get("config_folder_path")
        )
        self.__CONFIG_FILE_NAME = local_version_manager_cfg.get(
            "config_file_name"
        )

        try:
            config_file_format_in_cfg = local_version_manager_cfg.get(
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

        self.__CONFIG_FILE_FORMAT = config_file_format

    def save_config_txt(self, config, file_path: str) -> None:
        file_path += ".txt"
        with open(file_path, "w") as txt_file:
            txt_file.write(str(config))

    def save_config_json(self, config, file_path: str) -> None:
        file_path += ".json"
        with open(file_path, "w") as json_file:
            json.dump(config, json_file, indent=4)

    def save_config_yaml(self, config, file_path: str) -> None:
        file_path += ".yaml"
        with open(file_path, "w") as yaml_file:
            yaml.dump(
                config, yaml_file, default_flow_style=False, sort_keys=False
            )

    def save_configuration(
            self, config: dict[str, Any],
            output_format: ConfigFileFormat = None
    ) -> None:
        if not output_format:
            output_format = self.__CONFIG_FILE_FORMAT

        self.__CONFIG_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

        generic_file_path = os.path.join(
            self.__CONFIG_FOLDER_PATH, self.__CONFIG_FILE_NAME
        )
        datetime_stamp = datetime.now().isoformat(timespec="seconds")
        specific_file_path = f"{generic_file_path}_{datetime_stamp}"

        match output_format:
            case output_format.TXT:
                self.save_config_txt(config, specific_file_path)
            case output_format.JSON:
                self.save_config_json(config, specific_file_path)
            case output_format.YAML:
                self.save_config_yaml(config, specific_file_path)
