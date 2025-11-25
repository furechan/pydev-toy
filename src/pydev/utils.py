"""pydev utils"""

import os
import json
import tomli
import subprocess

from pathlib import Path

from functools import lru_cache

from packaging.version import Version

from urllib import request
from urllib.error import HTTPError


@lru_cache
def project_root(strict=False):
    """Walk up to find pyproject.toml"""

    cwd = Path.cwd()

    for path in cwd, *cwd.parents:
        if path.joinpath("pyproject.toml").exists():
            return path

    if strict:
        raise FileNotFoundError("pyproject.toml")


def run_command(command, *, cwd=None, echo=True, strict=False):
    """Run shell command"""

    if echo:
        print(command)

    rc = subprocess.run(command, cwd=cwd, shell=True)

    if strict and rc != 0:
        raise RuntimeError("Command failed!")



@lru_cache
def load_config():
    """Load pyproject.toml file"""

    root = project_root(strict=True)
    pyproject = root.joinpath("pyproject.toml").resolve(strict=True)

    with open(pyproject, "rb") as f:
        return tomli.load(f)


def get_config(item: str):
    """Query pyproject.toml file"""

    data = load_config()

    for i in item.split("."):
        data = data.get(i, None)
        if data is None:
            break

    return data


def search_path(pattern: str, path=None):
    """Search items in path"""

    if path is None:
        path = os.getenv("PATH")

    if isinstance(path, str):
        path = path.split(os.pathsep)
    if isinstance(path, os.PathLike):
        path = [path]

    for p in path:
        p = Path(p)
        yield from p.glob(pattern)


def confirm_choice(message):
    prompt = f"{message} (yes/no):"
    response = input(prompt)
    return response.lower() in ("y", "yes")
   


def pypi_releases(name):
    """List of version on pypi"""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = data.get("releases", [])
        return sorted(releases, key=Version, reverse=True)
    except HTTPError:
        return []


def bump_version(version):
    """Bump patch version"""
    if isinstance(version, str):
        version = Version(version)
    return f"{version.major}.{version.minor}.{version.micro + 1}"


def already_released():
    name = get_config("project.name")
    version = get_config("project.version")
    releases = pypi_releases(name)
    return version in releases

