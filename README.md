# Command line utils to manage simple python projects 

Set of command line utils to manage `pyproject.toml` based projects.
The command line is built with `click` and can run multiple project
related tasks in sequence from the command line.

```console
pydev clean build dump
```

This project is exploratory and may be found usefull as basis for custom workflows.
The project uses standard python packaging tools like `build` and `twine`
independently from any build backend like `setuptools`, `hatch`, `pdm`, etc ...


## Usage

```console
Usage: pydev [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  build    Build project wheel
  clean    Delete build and dist folders
  dump     Dump wheel and dist contents
  info     Project information
  prune    Delete all runtime folders
  publish  Publish project with twine
  pwd      Project root path
  which    Locate python by version and target
```


## Installation

The tool is best installed as a script in a separate ennvironment using `pipx` or `uv tool`.

```console
pipx install git+https://github.com/furechan/pydev-tool.git
```

## Related Projects & Resources
- [packaging_tools_comparisons](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html) Packaging tools comparisons
- [task_runners](https://sinoroc.gitlab.io/kb/python/task_runners.html) Python Task Runners
- [click](https://click.palletsprojects.com/) Python composable command line interface toolkit
- [build](https://github.com/pypa/build) A simple, correct Python build frontend
- [twine](https://github.com/pypa/twine/) Utilities for interacting with PyPI
