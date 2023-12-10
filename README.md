# Python cli prototype to manage simple projects 

Basic command line tool to manage standard `pyproject.toml` based projects.
This is a prototype cli built with `click` that can run multiple project
related tasks in sequence from the command line.

```console
pydev clean build dump
```

This project is exploratory and may be usefull as a template for custom workflows
when not commited yet to tool chains like `poetry`, `pdm`, `hatch`, etc ...

The script can be installed in a system/base python environment and
used in another project even if is is not installed in the project venv.

The script uses standard python packaging tools like `build` and `twine` and
is independent from the project build backend.


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
with the same name as other projects like
[pydev](https://pypi.org/project/pydev/).

You can install the latest version of this package with pip.

```console
pip install git+https://github.com/furechan/pydev-click.git
```

## Related Projects & Resources
- [packaging.python.org](https://packaging.python.org/en/latest/) Packaging User Guide
- [packaging_tools_comparisons](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html) Packaging tools comparisons
- [task_runners](https://sinoroc.gitlab.io/kb/python/task_runners.html) Python Task Runners
- [click](https://click.palletsprojects.com/) Python composable command line interface toolkit
- [invoke](https://www.pyinvoke.org/) Pythonic task management & command execution
- [build](https://github.com/pypa/build) A simple, correct Python build frontend
