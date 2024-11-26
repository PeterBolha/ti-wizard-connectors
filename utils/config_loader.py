import os
from typing import Any, Dict

import yaml


class ConfigLoader:
    __GLOBAL_CFG_PATH = "./app_config_templates/config_processors_cfg.yaml"

    @staticmethod
    def load_config() -> Dict[str, Any]:
        if not os.path.isfile(ConfigLoader.__GLOBAL_CFG_PATH):
            raise FileNotFoundError(
                f"Mandatory global config file was not found on path: '"
                f"{ConfigLoader.__GLOBAL_CFG_PATH}'"
            )

        with open(
            ConfigLoader.__GLOBAL_CFG_PATH, "r", encoding="utf-8"
        ) as yml_cfg:
            loaded_cfg = yaml.safe_load(yml_cfg)

        return loaded_cfg
