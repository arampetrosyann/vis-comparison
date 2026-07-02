#!/bin/bash

set -e

# pyenv should be installed and available
#
# pyenv install 3.7.9
# pyenv local 3.7.9

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -r "requirements_$1.txt"
