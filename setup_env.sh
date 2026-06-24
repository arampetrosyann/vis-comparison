#!/bin/bash

# pyenv should be installed and available
#
# pyenv install 3.7.9
# pyenv local 3.7.9

python3 -m venv .venv

source .venv/bin/activate

pip install -r "requirements_$1.txt"
