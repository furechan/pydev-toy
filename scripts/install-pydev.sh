#!/bin/bash

# Install pydev tool with pipx

set -eu

project_url="git+ssh://git@github.com/furechan/pydev-tool.git"

pipx install --force $project_url
