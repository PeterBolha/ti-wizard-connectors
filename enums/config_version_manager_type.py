from enum import Enum


# TODO - expand with more supported types such as GitLab, GitHub etc.
class ConfigVersionManagerType(Enum):
    LOCAL = ("LOCAL",)  # LOCAL file system
    GIT = "GIT"
