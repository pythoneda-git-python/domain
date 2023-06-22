"""
pythonedagitpython/git_repo_requested_for_python_package.py

This file defines the GitRepoRequestedForPythonPackage event class.

Copyright (C) 2023-today rydnr's pythoneda/git-repositories

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
from pythoneda.event import Event
from pythoneda.value_object import attribute, primary_key_attribute

from typing import Dict


class GitRepoRequestedForPythonPackage(Event):
    """
    Represents the event when a git repository has been requested for a given Python package.

    Class name: GitRepoRequestedForPythonPackage

    Responsibilities:
        - Represents the moment when the git repository of a Python package has been identified.

    Collaborators:
        - None
    """

    def __init__(
        self, packageName: str, packageVersion: str, info: Dict, release: Dict
    ):
        """
        Creates a new GitRepoRequestedForPythonPackage instance.
        :param packageName: The name of the Python package.
        :type packageName: str
        :param packageVersion: The version of the Python package.
        :type packageVersion: str
        :param info: The repository info.
        :type info: Dict
        :param release: The release info.
        :type release: Dict
        """
        self._package_name = packageName
        self._package_version = packageVersion
        self._info = info
        self._release = release

    @property
    @primary_key_attribute
    def package_name(self) -> str:
        """
        Retrieves the name of the Python package.
        :return: Such name.
        :rtype: str
        """
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self) -> str:
        """
        Retrieves the version of the Python package.
        :return: Such version.
        :rtype: str
        """
        return self._package_version

    @property
    @attribute
    def info(self) -> Dict:
        """
        Retrieves the Python package information.
        :return: Such metadata.
        :rtype: Dict
        """
        return self._info

    @property
    @attribute
    def release(self) -> Dict:
        """
        Retrieves the information about the Python package release.
        :return: Such information.
        :rtype: Dict
        """
        return self._release
