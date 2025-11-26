"""Tasks template for uv based projects"""

import json
from pathlib import Path
from urllib import request
from urllib.error import HTTPError

from invoke import task

ROOTDIR = Path(__file__).parent

TEMPLATE_URL = "https://raw.githubusercontent.com/furechan/pydev-toy/main/tasks.py"


def get_version(c) -> str:
    return c.run("uv version --short", hide=True).stdout.strip()


def parse_version(version: str) -> tuple:
    return tuple(int(part) if part.isdigit() else part for part in version.split("."))


def pypi_releases(name: str) -> list[str]:
    """List of releases from pypi"""
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = data.get("releases", [])
        releases = sorted(releases, key=parse_version, reverse=True)
        return releases
    except HTTPError:
        return []


def user_confirm(message: str, *, exit_otherwise=False) -> bool:
    """Confirm user choice or exit (optionally)"""
    response = input(f"{message} (y/N): ")
    confirm = response.lower() in ('y', 'yes')
    if exit_otherwise and not confirm:
        exit(1)
    return confirm


@task
def info(c):
    """Project info including pypi releases"""
    name, verion = c.run("uv version", hide=True).stdout.strip().split(" ")
    releases = pypi_releases(name)
    if len(releases) > 5:
        releases = releases[:5] + ["..."] 
    print("name:", name)
    print("version:", verion)
    print("releases:", *releases)


@task
def update(c, yes=False):
    """Update tasks.py from remote source"""
    if not yes:
        user_confirm(f"Update tasks.py from {TEMPLATE_URL}?", exit_otherwise=True)
    c.run(f"curl -fsSL {TEMPLATE_URL} -o {__file__}")


@task
def clean(c):
    """Clean project dist"""
    with c.cd(ROOTDIR):
        c.run("rm -f dist/*")


@task
def dump(c):
    """Dump wheel contents"""
    for file in ROOTDIR.glob("dist/*.whl"):
        c.run(f"unzip -l {file}")


@task(clean)
def build(c):
    """Build project wheel"""
    with c.cd(ROOTDIR):
        c.run("uv build --wheel")



@task(clean)
def release(c):
    """Build and publish package wheel"""

    git_found = ROOTDIR.joinpath(".git").exists()

    with c.cd(ROOTDIR):
        version = get_version(c)

        if git_found:
            # Fetch remote and ensure we're up to date
            c.run("git fetch -q")
            c.run("git rev-list --count @{u}..", hide=True)

        if 'dev' in version:
            # Bump to stable version
            c.run("uv version --bump stable")
            version = get_version(c)

        # Build Wheel
        c.run("uv build --wheel")

        # Commit and push changes
        if git_found:
            c.run(f"git commit -am 'Release {version}'")
            c.run("git push")

        # Publish to PyPI
        c.run("uv publish")

        # Bump to next dev version
        c.run("uv version --bump patch --bump dev=0")
        version = get_version(c)

        # Commit new dev version
        if git_found:
            c.run(f"git commit -am 'Bump to version {version}'")


