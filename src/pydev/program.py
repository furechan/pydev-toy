import os
import sys

import json
import click
import shutil
import logging
import subprocess

from urllib import request
from urllib.error import HTTPError

from pathlib import Path

from . import utils
from . import messages

logger = logging.getLogger()



@click.group(chain=True)
def main():
    pass


@main.command
def pwd():
    """ Project root path """
    utils.run_command("pwd", echo=False)

@main.command
def info():
    """ Project information """
    name = utils.get_config("project.name")
    version = utils.get_config("project.version")
    project_root = utils.get_project_root()
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
    root_project = utils.get_project_root(strict=True)
    folders = 'build', 'dist'

    for folder in folders:
        path = root_project.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
@click.option('-y', '--yes', is_flag=True)
def prune(yes):
    """ Delete all runtime folders """
    root_project = utils.get_project_root(strict=True)
    folders = 'build', 'dist', ".venv", ".nox", ".tox"
    confirm = yes or utils.confirm_choice(f"Do you want to delete runtime folders {folder}")

    if not confirm:
        exit(1)

    for folder in folders:
        path = root_project.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
@click.pass_context
def build(ctx):
    """ Build project wheel """
    # ctx.invoke(clean)
    python = utils.get_python()
    utils.run_command(f"{python} -m build --wheel")


@main.command
def dump():
    """ Dump wheel and dist contents """
    project_root = utils.get_project_root()
    dist = project_root.joinpath("dist")

    for file in dist.glob("*.whl"):
        utils.run_command(f"unzip -l {file}")

    for file in dist.glob("*.tar.gz"):
        utils.run_command(f"tar -ztvf {file}")


@main.command
@click.option('-t', '--test-pypi', is_flag=True)
def publish(test_pypi=False):
    """ Publish project with twine """
    if not utils.get_config("tool.pydev.allow-publish"):
        print(messages.ALLOW_PUBLISH)
        exit(1)

    python = utils.get_python()
    if test_pypi:
        command = f"{python} -mtwine upload --repository testpypi dist/*"
    else:
        command = f"{python} -mtwine upload dist/*"

    print(command)


@main.command
@click.argument('version', default='')
@click.option('--system', 'target', flag_value='system', default=True)
@click.option('--pyenv', 'target', flag_value='pyenv')
@click.option('--conda', 'target', flag_value='conda')
def which(version, target):
    """ Locate python by version and target """
    if python := utils.which_python(version, target):
        print(python)
    else:
        print(f"Python {version} for {target} not found!")
