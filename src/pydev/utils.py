"""pydev utils"""

import os
import json
import tomlkit
import subprocess

from pathlib import Path

from functools import lru_cache

from urllib import request
from urllib.error import HTTPError

from packaging.version import Version



def run_command(command: str, *, cwd=None, check=False, echo=True) -> int:
    """Run shell command"""

    if echo:
        print(command)

    res = subprocess.run(command, cwd=cwd, shell=True, check=check)

    return res.returncode



@lru_cache
def project_root(strict: bool = False) -> Path:
    """Walk up to find pyproject.toml"""

    cwd = Path.cwd()

    for path in cwd, *cwd.parents:
        if path.joinpath("pyproject.toml").exists():
            return path

    if strict:
        raise FileNotFoundError("pyproject.toml")


def project_file(name: str = "pyproject.toml") -> Path:
    """Get project file path"""

    root = project_root(strict=True)
    return root.joinpath(name)


def load_config() -> dict:
    """Load pyproject.toml file"""

    pyproject = project_file().resolve(strict=True)

    with open(pyproject, "r") as f:
        data = tomlkit.load(f)

    return data


def save_config(data: dict):
    """Save pyproject.toml file"""

    pyproject = project_file().resolve(strict=True)

    with open(pyproject, "w") as f:
        return tomlkit.dump(data, f)



def query_config(item: str):
    """Query pyproject.toml file"""

    data = load_config()

    for i in item.split("."):
        data = data.get(i, None)
        if data is None:
            break

    return data


def update_config(item: str, value):
    """Query pyproject.toml file"""

    data = load_config()

    if not data:
        raise RuntimeError("Could not load pyproject.toml!")

    parts = item.split(".")
    key = parts.pop()
    leaf = data

    for i in parts:
        leaf = leaf.get(i, None)
        if leaf is None:
            raise KeyError(f"Item {i} not found!")

    leaf[key] = value
    save_config(data)



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


def user_confirm(message: str, *, exit_otherwise=False) -> bool:
    prompt = f"{message} (yes/no):"
    response = input(prompt)
    confirm = response.lower() in ("y", "yes")
    if exit_otherwise and not confirm:
        exit(1)
    return confirm


def pypi_releases(name: str) -> list[str]:
    """List of version on pypi"""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = data.get("releases", [])
        return sorted(releases, key=Version, reverse=True)
    except HTTPError:
        return []



def stable_version(version) -> str:
    """Bump to stable version"""
    if isinstance(version, str):
        version = Version(version)
    return f"{version.major}.{version.minor}.{version.micro}"



def bump_version(version) -> str:
    """Bump patch version"""
    if isinstance(version, str):
        version = Version(version)
    return f"{version.major}.{version.minor}.{version.micro + 1}"


def already_released() -> bool:
    name = query_config("project.name")
    version = query_config("project.version")
    releases = pypi_releases(name)
    return version in releases

