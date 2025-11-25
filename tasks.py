"""
Tasks template for uv based projects
Requires `invoke` and `packaging` modules!
"""

from invoke import task
from pathlib import Path
from packaging.version import Version


TEMPLATE_URL = "https://raw.githubusercontent.com/furechan/pydev-toy/main/tasks.py"

ROOTDIR = Path(__file__).parent


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

    with c.cd(ROOTDIR):
        version = Version(c.run("uv version --short").stdout)

        if version.is_prerelease:
            c.run("uv version --bump stable")

        c.run("uv build --wheel")
        c.run("uv publish")

        version = bump_version(version) + ".dev0"

        c.run(f"uv version {version}")


