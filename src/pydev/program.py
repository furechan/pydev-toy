import os
import sys

import json
import click
import shutil
import logging

from urllib import request
from urllib.error import HTTPError

from .utils import get_project_root, get_config

from pathlib import Path

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
def root():
    """ Project root """
    run_command("pwd")


@main.command
def init():
    """ Inititalize Project env """
    run_command("pip install build twine pytest where-toy")


@main.command
def info():
    """ Project information """
    name = get_config("project.name")
    version = get_config("project.version")
    print("name", name)
    print("version", version)
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
    """ Clean build and dist folders """
    for folder in 'build', 'dist':
        path = Path(folder)
        if path.is_dir():
            print(f"rmtree {folder}")
            shutil.rmtree(path)


@main.command('build')
@click.pass_context
def build(ctx):
    """ Build project wheel """
    ctx.invoke(clean)
    run_command("python -m build --wheel")


@main.command('dump')
def dump():
    """ Dump wheel and dist contents """
    dist = Path("dist")

    for file in dist.glob("*.whl"):
        run_command(f"unzip -l {file}")

    for file in dist.glob("*.tar.gz"):
        run_command(f"tar -ztvf {file}")


@main.command('publish')
@click.option('-t', '--test-pypi')
def publish(test_pypi=False):
    """ Publish project with twine """
    if test_pypi:
        print("twine upload --repository testpypi dist/*")
    else:
        print("twine upload dist/*")
