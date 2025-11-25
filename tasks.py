"""
Tasks template for uv based projects
Requires `invoke` and `packaging` modules!
"""

from invoke import task
from pathlib import Path
from packaging.version import Version


TEMPLATE_URL = "https://raw.githubusercontent.com/furechan/pydev-toy/main/tasks.py"

ROOTDIR = Path(__file__).parent


def get_version(c) -> str:
    return Version(c.run("uv version --short", hide=True).stdout.strip())


def bump_version(version: str | Version) -> str:
    """Bump patch version"""
    if isinstance(version, str):
        version = Version(version)
    return f"{version.major}.{version.minor}.{version.micro + 1}"


@task
def update(c, yes=False):
    """Update tasks.py from remote source"""
    if not yes:
        response = input(f"Update tasks.py from {TEMPLATE_URL}? [y/N] ")
        if response.lower() not in ('y', 'yes'):
            print("Update cancelled.")
            return    
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
def publish(c):
    """Build and publish package wheel"""

    dotgit = ROOTDIR.joinpath(".git")

    with c.cd(ROOTDIR):
        version = get_version(c)

        if dotgit.exists():
            # Fetch remote and ensure we're up to date
            c.run("git fetch -q")
            c.run("git rev-list --count @{u}.. >/dev/null")

        if version.is_prerelease:
            # Bump to stable version
            c.run("uv version --bump stable")
            version = get_version(c)

        c.run("uv build --wheel")

        if dotgit.exists():
            c.run(f"git commit -am 'Release {version}'")
            c.run("git push")
 
        c.run("uv publish")
        c.run("uv version --bump patch --bump dev")
        version = get_version(c)

        if dotgit.exists():
            c.run(f"git commit -am 'Bump to version {version}'")


