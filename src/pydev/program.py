""" pydev program """

import json
import click
import shutil
import logging

from urllib import request
from urllib.error import HTTPError

from . import utils
from . import messages

logger = logging.getLogger()


@click.group(chain=True)
def main():
    pass


@main.command
def pwd():
    """ Run pwd """
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
    project_root = utils.get_project_root(strict=True)
    folders = 'build', 'dist'

    for folder in folders:
        path = project_root.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
@click.option('-y', '--yes', is_flag=True)
def prune(yes):
    """ Delete all runtime folders """
    project_root = utils.get_project_root(strict=True)
    folders = 'build', 'dist', ".venv", ".nox", ".tox"

    folders = [f for f in folders
               if project_root.joinpath(f).exists()]

    confirm = yes or utils.confirm_choice(f"Do you want to delete runtime folders {folders}")
    if not confirm:
        exit(1)

    for folder in folders:
        path = project_root.joinpath(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command
def build():
    """ Build project wheel """
    python = utils.get_python()
    project_root = utils.get_project_root()
    if project_root.joinpath("setup.py").exists():
        target = "sdist"
    else:
        target = "wheel"
    utils.run_command(f"{python} -m build --{target}")


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

    utils.run_command(command)


@main.command
@click.argument('version', default='')
@click.option('--system', 'target', flag_value='system', default=True, help="Use system python")
@click.option('--pyenv', 'target', flag_value='pyenv', help="Use pyenv version")
@click.option('--conda', 'target', flag_value='conda', help="Use conda env")
def which(version, target):
    """ Locate python by version and target """
    if python := utils.which_python(version, target):
        print(python)
    else:
        print(f"Python {version} for {target} not found!")
