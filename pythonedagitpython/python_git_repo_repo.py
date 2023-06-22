"""
pythonedagitpython/git_repo_repo.py

This file defines the GitRepoRepo class.

Copyright (C) 2023-today rydnr's pythoneda/git-python

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pythoneda.repo import Repo
from pythonedagitpython.python_git_repo import PythonGitRepo

import abc
from typing import Dict
import logging
import subprocess


class PythonGitRepoRepo(Repo, abc.ABC):
    """
    A subclass of Repo that manages Git repositories of Python projects.

    Class name: GitRepoRepo

    Responsibilities:
        - Implements a repository of PythonGitRepo instances.
        - Takes care of accessing information about PythonGitRepo instances.

    Collaborators:
        - It's a port. Adapters will have collaborators themselves.
    """

    def __init__(self):
        """
        Creates a new PythonGitRepoRepo instance.
        """
        super().__init__(GitRepo)

    @abc.abstractmethod
    def find_by_url_and_rev(self, url: str, revision: str) -> Dict[str, str]:
        """
        Retrieves the git repository for given url and revision.
        :param url: The url.
        :type url: str
        :param revision: The revision.
        :type revision: str
        :return: The git repository metadata.
        :rtype: Dict[str, str]
        """
        raise NotImplementedError(
            "find_by_url_and_rev() must be implemented by subclasses"
        )

    def fix_rev(self, url: str, rev: str, subfolder: str) -> str:
        """
        Tries to find out the actual revision for given rev value.
        :param url: The url.
        :type url: str
        :param rev: The initial revision to check for.
        :type rev: str
        :param subfolder: In case of a monorepo, the subfolder we're insterested in.
        :type subfolder: str
        :return: The fixed revision.
        :rtype: str
        """
        result = None
        owner, repo_name = PythonGitRepo.extract_repo_owner_and_repo_name(url)
        attempts = [rev, f"v{rev}", f"{repo_name}-{rev}", f"{repo_name}_{rev}"]
        if subfolder:
            # Attempting to support monorepos such as `azure-sdk-for-python`
            last_part_of_subfolder = subfolder.split("/")[-1]
            attempts.append(f"{last_part_of_subfolder}_{rev}")
            attempts.append(f"{last_part_of_subfolder}-{rev}")

        for tag in attempts:
            if self.revision_exists(url, tag):
                result = tag
                break

        if not result:
            result = self.get_latest_tag(url)

        return result

    @abc.abstractmethod
    def get_latest_tag(self, user: str, repo: str) -> str:
        """
        Retrieves the latest tag of given repository.
        :param user: The user.
        :type user: str
        :param repo: The repository.
        :type repo: str
        :return: The latest tag.
        :rtype: str
        """
        raise NotImplementedError("get_latest_tag() must be implemented by subclasses")
