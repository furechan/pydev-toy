#!/bin/zsh

# Install with pipx

set -eu

project_root=${o:a:h:h}

pipx install --force $project_root
