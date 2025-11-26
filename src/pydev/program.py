"""Basic python project management cli based on build and twine"""

import sys
import shutil
import logging
import tomlkit

import click

from . import utils
from . import messages

logger = logging.getLogger()


TASKS_SOURCE_URL = "https://raw.githubusercontent.com/furechan/pydev-toy/main/tasks.py"


@click.group(chain=True)
def main():
    pass


@main.command
def info():
    """Project info including pypi versions"""
    name = utils.query_config("project.name")
    version = utils.query_config("project.version")
    location = utils.project_root()
    releases = utils.pypi_releases(name)
    print("name", name)
    print("version", version)
    print("location", location)
    print("pypi.releases", releases)


@main.command
def tasks():
    """Inject tasks.py template into project"""

    root = utils.project_root(strict=True)
    tasks_py = root.joinpath("tasks.py")

    if tasks_py.exists():
        utils.user_confirm(
            "tasks.py already exists! Overwrite?",
            exit_otherwise=True
        )

    command = f"curl -fsSL {TASKS_SOURCE_URL} -o {tasks_py}"

    utils.run_command(command)


@main.command
def clean():
    """Deletes all dist files"""
    root = utils.project_root(strict=True)
    dist = root.joinpath("dist")
    for f in dist.glob("*.whl"):
        print(f"unlink {f.name}")
        f.unlink()



@main.command
@click.option("-y", "--yes", is_flag=True)
def prune(yes):
    """Delete all runtime folders"""
    root = utils.project_root(strict=True)
    folders = "build", "dist", ".venv", ".nox", ".tox"
    folders = [f for f in folders if root.joinpath(f).exists()]

    if not yes:
        utils.user_confirm(
            f"Do you want to delete runtime folders {folders}",
            exit_otherwise=True
        )

    for folder in folders:
        path = root.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)



@main.command
def dump():
    """Dump wheel and sdist contents"""
    root = utils.project_root(strict=True)
    dist = root.joinpath("dist")

    for file in dist.glob("*.whl"):
        utils.run_command(f"unzip -l {file}")

    for file in dist.glob("*.tar.gz"):
        utils.run_command(f"tar -ztvf {file}")


@main.command
@click.option("-d", "--dev", is_flag=True)
def bump(dev=False):
    """Bump patch version in pyproject"""
    root = utils.project_root(strict=True)
    pyproject = root.joinpath("pyproject.toml").resolve(strict=True)
    config = tomlkit.loads(pyproject.read_text())
    version = config["project"]["version"]

    version = utils.bump_version(version)
    if dev:
        version = version + ".dev0"

    config["project"]["version"] = str(version)

    print(f"Updating version to {version} ...")
    pyproject.write_text(tomlkit.dumps(config))



@main.command
@click.option("-c", "--clean", is_flag=True)
def build(clean=False):
    """Build project wheel"""

    python = sys.executable
    root = utils.project_root(strict=True)
    dist = root.joinpath("dist")

    # clean dist folder if present
    if clean and dist.is_dir():
        print(f"rmtree {dist}")
        shutil.rmtree(dist)

    # pick target depending on setup config
    if root.joinpath("setup.py").exists():
        target = "sdist"
    else:
        target = "wheel"

    utils.run_command(f"{python} -m build --{target}")



@main.command
@click.pass_context
@click.option("-t", "--test-pypi", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def publish(ctx, test_pypi=False, verbose=False):
    """Publish project to pypi"""

    if not utils.query_config("tool.pydev.allow-publish"):
        print(messages.ALLOW_PUBLISH)
        exit(1)

    python = sys.executable

    flags = ""
    if test_pypi:
        flags += " --repository testpypi"
    if verbose:
        flags += " --verbose"

    command = f"{python} -mtwine upload {flags} dist/*"

    utils.run_command(command)



@main.command
@click.pass_context
@click.option("-t", "--test-pypi", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
def release(ctx, test_pypi=False, verbose=False):
    """Build and publish project to pypi"""

    version = utils.query_config("project.version")
    if "dev" in version:
        print("Cannot release a dev version!")
        exit(1)

    if not utils.query_config("tool.pydev.allow-publish"):
        print(messages.ALLOW_PUBLISH)
        exit(1)

    python = sys.executable

    flags = ""
    if test_pypi:
        flags += " --repository testpypi"
    if verbose:
        flags += " --verbose"

    command = f"{python} -mtwine upload {flags} dist/*"

    utils.run_command(command)


