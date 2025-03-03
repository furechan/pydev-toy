# noinspection PyUnresolvedReferences

import re

from pathlib import Path
from invoke import task  # type: ignore

ROOT = Path(__file__).parent


@task
def clean(ctx):
    """Clean project dist"""
    ctx.run("rm -rf dist")


@task
def check(ctx):
    """Check package"""
    ctx.run("ruff check")


@task(clean)
def build(ctx):
    """Build project wheel"""
    ctx.run("python -mbuild --wheel")


@task
def dump(ctx):
    """Dump wheel contents"""
    for file in ROOT.glob("dist/*.whl"):
        ctx.run(f"unzip -l {file}")


@task
def publish(ctx, testpypi=False):
    """Publish to PyPI with twine"""
    flags = "--repository testpypi" if testpypi else ""
    ctx.run(f"twine upload {flags} dist/*.whl")


@task
def bump(ctx):
    """Bump patch version in pyproject"""
    pyproject = ROOT.joinpath("pyproject.toml").resolve(strict=True)
    buffer = pyproject.read_text()
    pattern = re.compile(r"(?mx)^version \s* = \s* \"(.+)\" \s*")
    match = pattern.search(buffer)
    if not match:
        raise ValueError("Could not find version setting")
    version = tuple(int(i) for i in match.group(1).split("."))
    version = version[:-1] + (version[-1] + 1,)
    version = ".".join(str(v) for v in version)
    print(f"Updating version to {version} ...")
    output = pattern.sub(f'version = "{version}"\n', buffer)
    pyproject.write_text(output)
