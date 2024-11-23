# Python cli prototype to manage simple projects 

Set of command line utils to manage `pyproject.toml` based projects.
The command line is built with `click` and can run multiple project
related tasks in sequence from the command line.

```console
pydev clean build dump
```

This project is exploratory and may be usefull as basis for custom workflows
independently from backend specific tools like `poetry`, `pdm`, `hatch`, etc ...

The script uses only standard python packaging tools like `build` and `twine` and
is independent from any project build backends.


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

> **Warning**
This project installs a script called `pydev`
which is the same name as other projects like
[pydev](https://pypi.org/project/pydev/).

You can install the latest version of this package with `pip` or `pipx`.

```console
pipx install git+ssh://git@github.com/furechan/pydev-tool.git
```

## Related Projects & Resources
- [packaging_tools_comparisons](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html) Packaging tools comparisons
- [task_runners](https://sinoroc.gitlab.io/kb/python/task_runners.html) Python Task Runners
- [click](https://click.palletsprojects.com/) Python composable command line interface toolkit
- [build](https://github.com/pypa/build) A simple, correct Python build frontend
- [twine](https://github.com/pypa/twine/) Utilities for interacting with PyPI
