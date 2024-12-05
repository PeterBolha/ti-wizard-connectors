import os
from datetime import datetime
from pathlib import Path
from typing import Any

from config_version_managers.file_config_version_manager import (
    FileConfigVersionManager,
)
from enums.config_file_format import ConfigFileFormat


class LocalConfigVersionManager(FileConfigVersionManager):
    def __init__(self, local_version_manager_cfg):
        super().__init__(local_version_manager_cfg)

        self.__CONFIG_FOLDER_PATH = Path(
            local_version_manager_cfg.get("config_folder_path")
        )

    def save_configuration(
        self, config: dict[str, Any], output_format: ConfigFileFormat = None
    ) -> None:
        self.__CONFIG_FOLDER_PATH.mkdir(parents=True, exist_ok=True)

        generic_file_path = os.path.join(
            self.__CONFIG_FOLDER_PATH, self._CONFIG_FILE_NAME
        )
        datetime_stamp = datetime.now().isoformat(timespec="seconds")
        specific_file_path = f"{generic_file_path}_{datetime_stamp}"

        self.save_config_to_file(specific_file_path, config, output_format)
