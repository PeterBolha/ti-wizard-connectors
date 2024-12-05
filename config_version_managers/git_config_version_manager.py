import os
from datetime import datetime
from pathlib import Path
from typing import Any

from dulwich import porcelain
from dulwich.errors import NotGitRepository
from dulwich.porcelain import status
from dulwich.repo import Repo

from config_version_managers.file_config_version_manager import \
    FileConfigVersionManager


class GitConfigVersionManager(FileConfigVersionManager):
    def __init__(self, git_version_manager_cfg):
        super().__init__(git_version_manager_cfg)

        self.__GIT_REPO_FOLDER_PATH = Path(
            git_version_manager_cfg.get("git_repo_folder_path")
        )
        self.__GIT_BRANCH_NAME = git_version_manager_cfg.get("git_branch_name")
        self.__COMMITTER = git_version_manager_cfg.get("committer")

        self.__GIT_REPO = git_version_manager_cfg.get("git_repo")
        self.__GIT_USERNAME = git_version_manager_cfg.get("git_username")
        self.__GIT_TOKEN = git_version_manager_cfg.get("git_token")

    def set_target_branch(self, repo: Repo) -> None:
        branches = repo.get_refs()
        branch_ref = f"refs/heads/{self.__GIT_BRANCH_NAME}".encode()

        if branch_ref not in branches:
            current_head = repo.head()
            repo.refs[branch_ref] = current_head

        repo.refs.set_symbolic_ref(b"HEAD", branch_ref)

    # TODO refine the check of encoded/unencoded files
    def has_file_changed(self, repo: Repo, file_path: str) -> bool:
        repo_status = status(repo)

        staged_items = [
            item for sublist in repo_status.staged.values() for item in sublist
        ]
        changed_files = (
                staged_items
                + repo_status.unstaged  # Staged for commit
                + repo_status.untracked
        # Modified but not staged  # Untracked files
        )

        file_name = os.path.basename(file_path)
        observed_files = [file_name.encode(), file_name]

        for observed_file in observed_files:
            if observed_file in changed_files:
                return True

        return False

    def get_repo(self) -> Repo:
        try:
            repo = Repo(str(self.__GIT_REPO_FOLDER_PATH))
        except NotGitRepository:
            repo = porcelain.clone(
                source=self.__GIT_REPO,
                target=self.__GIT_REPO_FOLDER_PATH,
                username=self.__GIT_USERNAME,
                password=self.__GIT_TOKEN,
            )
        finally:
            self.set_target_branch(repo)

        return repo

    def publish_file_to_git(self, repo: Repo, file_path: str) -> None:
        # ADD changes
        porcelain.add(repo=repo, paths=[file_path])

        # COMMIT changes
        datetime_stamp = datetime.now().isoformat(timespec="seconds")
        commit_msg = f"Config change on {datetime_stamp}".encode()
        committer = self.__COMMITTER.encode()
        porcelain.commit(repo=repo, message=commit_msg, committer=committer)

        # PUSH changes
        porcelain.push(
            repo,
            remote_location=self.__GIT_REPO,
            username=self.__GIT_USERNAME,
            password=self.__GIT_TOKEN,
        )

    def save_configuration(self, config: dict[str, Any]) -> None:
        cfg_file_path = os.path.join(
            self.__GIT_REPO_FOLDER_PATH, self._CONFIG_FILE_NAME
        )
        repo = self.get_repo()

        saved_config_file_path = self.save_config_to_file(cfg_file_path, config)

        if self.has_file_changed(repo, saved_config_file_path):
            self.publish_file_to_git(repo, saved_config_file_path)
