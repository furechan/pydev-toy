# ---- noinspection PyUnresolvedReferences


from pathlib import Path

from packaging.version import Version

from invoke import task  # --- type: ignore


ROOTDIR = Path(__file__).parent


def bump_version(version):
    """Bump patch version"""
    if isinstance(version, str):
        version = Version(version)
    return f"{version.major}.{version.minor}.{version.micro + 1}"



@task
def pwd(c):
    """Print working directory"""
    c.run("pwd")



@task
def clean(c):
    """Clean project dist"""
    c.run("rm -f dist/*")



@task
def dump(c):
    """Dump wheel contents"""
    for file in ROOTDIR.glob("dist/*.whl"):
        c.run(f"unzip -l {file}")


@task(clean)
def build(c):
    """Build project wheel"""
    c.run("uv build --wheel")



@task(clean)
def publish(c):
    """Build and publish package wheel"""

    with c.cd(ROOTDIR):
        version = Version(c.run("uv version --short", hide=True).stdout)
        print(version, version.base_version)

        if version.is_prerelease:
            c.run("uv version --bump stable")

        c.run("uv build --wheel")
        c.run("uv publish")

        version = bump_version(version) + ".dev0"

        c.run(f"uv version {version}")

