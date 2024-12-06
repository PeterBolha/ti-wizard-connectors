from enum import Enum


class ConfigVersionManagerType(Enum):
    LOCAL = ("LOCAL",)  # LOCAL file system
    GIT = "GIT"
