from distutils.core import setup
setup(
    name = "pythoneda-git-repositories",
    packages = ["."],
#    packages = find_packages(),
    version = "0.0.1a1",
    description = "Git repositories in PythonEDA",
    author = "rydnr",
    author_email = "github@acm-sl.org",
    url = "https://github.com/rydnr/pythoneda-git-repositories",
    download_url = "https://github.com/rydnr/pythoneda-git-repositories/releases",
    keywords = ["eda", "ddd"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires=[
    ],
    long_description = """\
Git repositories in PythonEDA
-----------------------------

This package includes the domain of Git repositories in PythonEDA.

This is what this package  provides:
- PythonEDAGitRepositories/git_repo: A representation of Git repositories.
- PythonEDAGitRepositories/git_repo_repo: A repository to retrieve instances of GitRepo.
- PythonEDAGitRepositories/*: errors related to git operations.
""",
    tests_require=['pytest']
)
