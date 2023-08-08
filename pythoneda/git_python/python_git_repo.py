"""
pythoneda/git_python/python_git_repo.py

This file defines the PythonGitRepo class.

Copyright (C) 2023-today rydnr's pythoneda-git-python/domain

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
import abc
from pythoneda import attribute
from pythoneda.shared.git import GitRepo
from typing import Dict

class PythonGitRepo(GitRepo, abc.ABC):
    """
    Represents a Git repository of a Python project.

    Class name: PythonGitRepo

    Responsibilities:
        - Represents a git repository and its metadata.

    Collaborators:
        - None
    """

    def __init__(self, url: str, rev: str, repoInfo: Dict, subfolder=None):
        """
        Creates a new Git repository instance for a Python project.
        :param url: The url of the repository.
        :type url: str
        :param rev: The revision.
        :type rev: str
        :param repoInfo: The repository metadata.
        :type repoInfo: Dict
        :param subfolder: Whether it's a monorepo and we're interested only in a subfolder.
        :type subfolder: str
        """
        super().__init__(url, rev)
        self._repo_info = repoInfo
        self._subfolder = subfolder
        self._files = {}

    @property
    @attribute
    def repo_info(self) -> Dict:
        """
        Retrieves the repository metadata.
        :return: Such metadata.
        :rtype: Dict
        """
        return self._repo_info

    def is_monorepo(self) -> bool:
        """
        Checks whether this repository is a monorepo.
        :return: True in such case.
        :rtype: bool
        """
        return self._subfolder is not None

    def get_file(self, fileName: str) -> str:
        """
        Retrieves the contents of given file in the repo.
        :param fileName: The name of the file.
        :type fileName: str
        :return: The file contents.
        :rtype: str
        """
        result = self._files.get(fileName, None)
        if not result:
            result = self.access_file(fileName)
            self._files[fileName] = result

        return result

    @property
    @attribute
    def subfolder(self) -> str:
        """
        Retrieves the subfolder within the repository.
        :return: Such value.
        :rtype: str
        """
        return self._subfolder

    @abc.abstractmethod
    def access_file(self, fileName: str) -> str:
        """
        Accesses given file in the repo.
        :param fileName: The name of the file.
        :type fileName: str
        :return: The file information.
        :rtype: str
        """
        raise NotImplementedError("access_file() must be implemented by subclasses")
