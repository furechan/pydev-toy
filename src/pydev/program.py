import os
import sys

import json
import click
import shutil
import logging

from urllib import request
from urllib.error import HTTPError

from pathlib import Path

from . import messages

from .utils import get_project_root, get_python, get_config, which_python

logger = logging.getLogger()


# NOTE Script will chgdir to the project root at startup in main() !


def run_command(command, echo=True, strict=False):
    if echo:
        print(command)
    rc = os.system(command)
    if strict and rc != 0:
        raise RuntimeError("Command failed!")


@click.group(chain=True)
def main():
    project_root = get_project_root()
    if project_root:
        os.chdir(project_root)
    else:
        print("Project root not found!", file=sys.stderr)
        exit(1)


@main.command
def info():
    """ Project information """
    name = get_config("project.name")
    version = get_config("project.version")
    project_root = get_project_root()
    print("name", name)
    print("version", version)
    print("location", project_root)
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        res = request.urlopen(url)
        data = json.load(res)
        releases = list(data["releases"])
        print("pypi.releases", releases)
    except HTTPError:
        pass


@main.command
def clean():
    """ Delete build and dist folders """
    folders = 'build', 'dist'
    for folder in folders:
        path = Path(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
def reset():
    """ Delete all runtime folders (build, dist, .venv, .nox, .tox) """
    folders = 'build', 'dist', ".venv", ".nox", ".tox"
    for folder in folders:
        path = Path(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command('build')
@click.pass_context
def build(ctx):
    """ Build project wheel """
    ctx.invoke(clean)
    python = get_python()
    run_command(f"{python} -m build --wheel")


@main.command('dump')
def dump():
    """ Dump wheel and dist contents """
    dist = Path("dist")

    for file in dist.glob("*.whl"):
        run_command(f"unzip -l {file}")

    for file in dist.glob("*.tar.gz"):
        run_command(f"tar -ztvf {file}")


@main.command('publish')
@click.option('-t', '--test-pypi', is_flag=True)
def publish(test_pypi=False):
    """ Publish project with twine """
    if not get_config("tool.pydev.allow-publish"):
        print(messages.ALLOW_PUBLISH)
        exit(1)

    python = get_python()
    if test_pypi:
        command = f"{python} -mtwine upload --repository testpypi dist/*"
    else:
        command = f"{python} -mtwine upload dist/*"

    print(command)


@main.command('which')
@click.argument('version', default='')
@click.option('--system', 'target', flag_value='system', default=True)
@click.option('--pyenv', 'target', flag_value='pyenv')
@click.option('--conda', 'target', flag_value='conda')
def which(version, target):
    """ Locate python by version and target """
    if python := which_python(version, target):
        print(python)
    else:
        print(f"Python {version} for {target} not found!")
