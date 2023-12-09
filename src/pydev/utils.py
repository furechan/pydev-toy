import os
import tomli

from pathlib import Path

from functools import lru_cache


@lru_cache
def get_project_root():
    """ Walk up to find project root """

    def check_project(folder):
        return folder.joinpath("pyproject.toml").exists()

    work_dir = Path.cwd()

    if check_project(work_dir):
        return work_dir
    for path in work_dir.parents:
        if check_project(path):
            return path


@lru_cache
def load_config():
    """ Load pyproject.toml file """

    pyproject = Path("pyproject.toml").resolve(strict=True)

    with pyproject.open("rb") as f:
        return tomli.load(f)


def get_config(item: str, default=None):
    """ Query pyproject.toml file """

    data = load_config()

    for i in item.split("."):
        data = data.get(i, None)
        if data is None:
            return default

    return data


def search_path(pattern: str, path=None):
    """ Search items in path """

    if path is None:
        path = os.getenv("PATH")
    if isinstance(path, str):
        path = path.split(os.pathsep)
    if isinstance(path, os.PathLike):
        path = [path]

    for p in path:
        p = Path(p)
        yield from p.glob(pattern)


def system_python(version=None):
    if not version:
        version = "3"

    path = os.getenv("PATH", "/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin)"
    path = path.split(os.pathsep)

    pattern = "python" + version
    items = [i for p in path for i in Path(p).glob(pattern)]

    return next(items, None)


def pyenv_versions():
    """ pyenv versions """

    pyenv_root = os.getenv("PYENV_ROOT", "~/.pyenv")
    pyenv_root = Path(pyenv_root).expanduser()

    return pyenv_root.glob("versions/*")


def pyenv_python(version: str = None) -> Path:
    """ pyenv binary for target version """

    if not version:
        version = "3.*"
    elif version.count(".") < 2:
        version += ".*"

    pyenv_root = os.getenv("PYENV_ROOT", "~/.pyenv")
    pyenv_root = Path(pyenv_root).expanduser()

    if not pyenv_root.exists():
        return None

    pattern = f"versions/{version}/bin/python"

    return next(pyenv_root.glob(pattern), None)


def conda_envs():
    """ conda environments """

    conda_root = os.getenv("CONDA_PREFIX", "~/miniconda3")
    conda_root = Path(conda_root).expanduser()

    return [
        p for p in conda_root.glob("envs/*")
        if p.joinpath("bin/python").exists()
    ]


def conda_python(name: str = None) -> Path:
    """ conda binary for target version """

    conda_root = os.getenv("CONDA_PREFIX", "~/miniconda3")
    conda_root = Path(conda_root).expanduser()

    if name:
        conda_env = conda_root.joinpath(f"envs/{name}")
    else:
        conda_env = conda_root

    if conda_env.exists():
        return conda_env.joinpath("bin/python")


def get_python(version=None, target=None):
    if target == "pyenv":
        return pyenv_python(version)

    if target == "conda":
        return conda_python(version)

    if target in ("system", None):
        return system_python(version)
