# Command line helper to manage modern python projects 

Command line helper to manage standard `pyproject.toml` based projects.
The interface is built with `click` and can run multiple commands in sequence.

```shell
pydev clean build dump
```

This project is exploratory and may be usefull as a basis for custom workflows.

## Usage

```console
Usage: python -m pydev [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  build    Build project wheel
  bump     Bump version in pyproject
  clean    Deletes all dist files
  dump     Dump wheel and sdist contents
  info     Project info including pypi releases
  prune    Delete all runtime folders
  publish  Publish project to pypi
  release  Build and publish project to pypi
  tasks    Inject tasks.py template into project
```


## Installation

The `pydev` tool is best installed as a script in a separate ennvironment using `pipx` or `uv tool`.

```shell
pipx install pydev-toy
```

## Related Projects & Resources
- [Packaging tools](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html)
Comparison of different packaging tools
- [uv](https://github.com/astral-sh/uv)
An extremely fast Python package and project manager, written in Rust
- [hatch](https://hatch.pypa.io/latest/)
Hatch is a modern, extensible Python project manager
- [pdm](https://pdm-project.org/en/latest/)
Modern Python package and dependency manager supporting the latest PEP standards 
- [click](https://click.palletsprojects.com/)
Python composable command line interface toolkit
- [build](https://github.com/pypa/build)
A simple, correct Python build frontend
- [twine](https://github.com/pypa/twine/)
Utilities for interacting with PyPI
- [slap](https://github.com/NiklasRosenstein/slap)
CLI to assist in the process for developing and releasing Python packages
