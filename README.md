# Command line util to manage python projects 

Set of command line utils to manage standard `pyproject.toml` based projects.
The tool `pydev` is built with `click` and can run multiple commands in sequence.

```console
pydev clean build dump
```

This project is exploratory and may be found usefull as basis for custom workflows.
The project uses standard python packaging tools like `build` and `twine`
independently from any build backend like `setuptools`, `hatch`, `pdm`, etc ...


## Usage

```console
Usage: python -m pydev [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  build    Build project wheel
  bump     Bump static version in pyproject.toml
  clean    Delete build and dist folders
  dump     Dump wheel and sdist contents
  info     Project info including pypi versions
  prune    Delete all runtime folders
  publish  Publish project with twine
```


## Installation

The `pydev` tool is best installed as a script in a separate ennvironment using `pipx` or `uv tool`.

```console
pipx install pydev-toy
```

## Related Projects & Resources
- [Packaging tools](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html) Comparison of different packaging tools
- [setuptools](https://setuptools.pypa.io/en/latest/) Setuptools is a fully-featured, actively-maintained, and stable library designed to facilitate packaging Python projects.
- [hatch](https://hatch.pypa.io/latest/) Hatch is a modern, extensible Python project manager.
- [pdm](https://pdm-project.org/en/latest/) Modern Python package and dependency manager supporting the latest PEP standards 
- [click](https://click.palletsprojects.com/) Python composable command line interface toolkit
- [build](https://github.com/pypa/build) A simple, correct Python build frontend
- [twine](https://github.com/pypa/twine/) Utilities for interacting with PyPI
