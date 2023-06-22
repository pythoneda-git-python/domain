"""
pythonedagitpython/python_git_repo_found.py

This file defines the PythonGitRepoFound event class.

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
from pythoneda.event import Event
from pythoneda.value_object import attribute, primary_key_attribute

from typing import Dict


class PythonGitRepoFound(Event):
    """
    Represents the event when a git repository has been found for a Python package.

    Class name: GitRepoFound

    Responsibilities:
        - Represents the git repository of a Python package has been identified.

    Collaborators:
        - None
    """

    def __init__(
        self,
        packageName: str,
        packageVersion: str,
        url: str,
        tag: str,
        metadata: Dict,
        subfolder: str,
    ):
        """
        Creates a new PythonGitRepoFound instance.
        :param packageName: The Python package name.
        :type packageName: str
        :param packageVersion: The Python package version.
        :type packageVersion: str
        :param url: The repository url.
        :type url: str
        :param tag: The repository tag.
        :type tag: str
        :param metadata: The package metadata.
        :type metadata: Dict
        :param subfolder: If the repository is a monorepo, the subfolder within the repository.
        :type subfolder: str
        """
        super().__init__()
        self._package_name = packageName
        self._package_version = packageVersion
        self._url = url
        self._tag = tag
        self._metadata = metadata
        self._subfolder = subfolder

    @property
    @primary_key_attribute
    def package_name(self) -> str:
        """
        Retrieves the Python package name.
        :return: Such name.
        :rtype: str
        """
        return self._package_name

    @property
    @primary_key_attribute
    def package_version(self) -> str:
        """
        Retrieves the Python package version.
        :return: Such version.
        :rtype: str
        """
        return self._package_version

    @property
    @primary_key_attribute
    def url(self) -> str:
        """
        Retrieves the repository url.
        :return: Such value.
        :rtype: str
        """
        return self._url

    @property
    @primary_key_attribute
    def tag(self):
        """
        Retrieves the tag.
        :return: Such tag.
        :rtype: str
        """
        return self._tag

    @property
    @attribute
    def metadata(self):
        return self._metadata

    @property
    @attribute
    def subfolder(self) -> str:
        """
        Retrieves the subfolder, in case of a monorepo.
        :return: Such subfolder.
        :rtype: str
        """
        return self._subfolder
