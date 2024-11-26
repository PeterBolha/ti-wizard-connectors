from config_version_managers.config_version_manager import ConfigVersionManager
from config_version_managers.local_config_version_manager import (
    LocalConfigVersionManager,
)
from enums.config_version_manager_type import ConfigVersionManagerType


class ConfigVersionManagerInitializer:
    def __init__(self, config_version_manager_cfg):
        self.__VERSION_MANAGER_CFG = config_version_manager_cfg

    def get_config_version_manager(self) -> ConfigVersionManager:
        try:
            version_manager_type_in_cfg = self.__VERSION_MANAGER_CFG.get("type")
            version_manager_type = ConfigVersionManagerType[version_manager_type_in_cfg]
        except KeyError:
            raise ValueError(
                f"Invalid version manager type '{version_manager_type_in_cfg}' in configuration. "
                f"Allowed values are: {', '.join([e.name for e in ConfigVersionManagerType])}"
            )

        match version_manager_type:
            case ConfigVersionManagerType.LOCAL:
                return LocalConfigVersionManager(self.__VERSION_MANAGER_CFG)
