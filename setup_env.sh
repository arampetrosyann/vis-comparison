#!/bin/bash

set -euo pipefail

# pyenv should be installed and available
#
# pyenv install 3.7.9
# pyenv local 3.7.9

TOOL_NAME="${1:-}"

if [[ -z "$TOOL_NAME" ]]; then
	echo "Usage: $0 <tool-name>"
	exit 1
fi

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -r "requirements_${TOOL_NAME}.txt"

if [[ "$TOOL_NAME" == "data2vis" ]]; then
	python -m pip install -r vendor/data2vis/requirements.txt

	python -c "import tensorflow as tf; print(tf.__version__)"
fi
