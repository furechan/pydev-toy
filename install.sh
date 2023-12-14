#!/bin/zsh

set -eu

project=${0:a:h}

echo $project=$project

if [ -f $project/pyproject.toml ]
then
  pipx install $project
else
  echo pyproject.toml file not found!
  exit 1
fi



