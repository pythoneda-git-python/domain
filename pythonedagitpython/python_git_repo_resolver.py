"""
pythonedagitpython/git_repo_resolver.py

This file defines the PythonGitRepoResolver event listener class.

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
from pythoneda.event_listener import EventListener
from pythonedaeventgitpython.python_git_repo_found import PythonGitRepoFound
from pythonedaeventgitpython.git_repo_requested_for_python_package import GitRepoRequestedForPythonPackage
from pythonedagitpython.python_git_repo import PythonGitRepo

import asyncio
import logging
from typing import Dict, List, Type


class PythonGitRepoResolver(EventListener):
    """
    Resolves Git repositories for Python projects.

    Class name: PythonGitRepoResolver

    Responsibilities:
        - Resolves git repositories.
        - Listens for GitRepoRequestedForPythonPackage events.

    Collaborators:
        - GitRepoRequestedForPythonPackage: Triggers this class to resolve git repositories.
    """

    @classmethod
    def supported_events(cls) -> List[Type[Event]]:
        """
        Retrieves the list of supported event classes.
        :return: The list of supported events.
        :rtype: List
        """
        return [GitRepoRequestedForPythonPackage]

    @classmethod
    def fix_url(cls, url: str) -> str:
        """
        Fixes given repository url.
        :param url: The respository url.
        :type url: str
        :return: The fixed url.
        :rtype: str
        """
        result = url
        if result.endswith("/issues"):
            result = result.removesuffix("/issues")
        return result

    @classmethod
    def extract_urls(cls, info: Dict) -> List[str]:
        """
        Extracts the urls from the metadata of the Python project.
        :param info: The metadata.
        :type info: Dict
        :return: The list of urls.
        :rtype: List[str]
        """
        result = []
        project_urls = info.get("project_urls", {})
        for url in [
            entry["collection"].get(entry["key"], None)
            for entry in [
                {"collection": info, "key": "package_url"},
                {"collection": info, "key": "home_page"},
                {"collection": info, "key": "project_url"},
                {"collection": info, "key": "release_url"},
                {"collection": project_urls, "key": "Source"},
                {"collection": project_urls, "key": "Source Code"},
                {"collection": project_urls, "key": "Home"},
                {"collection": project_urls, "key": "Homepage"},
                {"collection": project_urls, "key": "Changelog"},
                {"collection": project_urls, "key": "Documentation"},
                {"collection": project_urls, "key": "Issue Tracker"},
                {"collection": project_urls, "key": "Tracker"},
            ]
        ]:
            if url:
                result.append(cls.fix_url(url))
        return result

    @classmethod
    async def listenGitRepoRequested(cls, event: GitRepoRequestedForPythonPackage) -> PythonGitRepo:
        """
        Gets notified when a GitRepoRequestedForPythonPackage event is emitted.
        :param event: The event.
        :type event: GitRepoRequestedForPythonPackage
        :return: The PythonGitRepo found, if any.
        :rtype: PythonGitRepo
        """
        for url in cls.extract_urls(event.info):
            repo_url, subfolder = GitRepo.extract_url_and_subfolder(url)
            if PythonGitRepo.url_is_a_git_repo(repo_url):
                asyncio.ensure_future(
                    cls.emit(
                        PythonGitRepoFound(
                            event.package_name,
                            event.package_version,
                            repo_url,
                            subfolder,
                        )
                    )
                )
                break
        logging.getLogger(__name__).warn(
            f"I couldn't obtain a git repo url from the project's urls"
        )
