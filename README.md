# Python cli prototype to manage simple projects 

Basic command line to manage standard `pyproject.toml` based projects.
This is a prototype cli built with `click` that allows to specify
multiple targets on the command line like:

```console
pydev init build dump
```

This may be usefull as a template for a custom workflow
if you are not ready to commit to specific tool chains
like `poetry`, `pdm`, `hatch`, etc ...

The script can be installed in you python system environment and used in any projects.
The script will look for the project root by walking up from the working directory
until it finds a `pyproject.toml` file.

To install the required dependencies (`build`, `twine`) in a target python environment
run `pydev init` before other commands. Please note the target environment must be the active environment.

The script uses standard python packaging tools like `build` and `twine` and
is independent from the project build backend.

## Usage


```console
Usage: pydev [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  build    Build project wheel
  clean    Clean build and dist folders
  dump     Dump wheel and dist contents
  info     Project information
  init     Inititalize current env
  publish  Publish project with twine
```


## Installation

> **Warning**
This project installs a script called `pydev`
which name is also used by other projects like
[pydev](https://pypi.org/project/pydev/).

You can install the latest version of this module with pip

```console
pip install git+https://github.com/furechan/pydev-proto.git
```

## Related projects and resources

- [Packaging tools comparisons](https://sinoroc.gitlab.io/kb/python/packaging_tools_comparisons.html)
- [Python task runners](https://sinoroc.gitlab.io/kb/python/task_runners.html)
- [click](https://click.palletsprojects.com/) Python composable command line interface toolkit
- [invoke](https://www.pyinvoke.org/) Pythonic task management & command execution
- [build](https://github.com/pypa/build) A simple, correct Python build frontend
