#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'

# AutoViz
if [ ! -d vendor/AutoViz/.git ]; then
	git clone https://github.com/AutoViML/AutoViz.git vendor/AutoViz
fi
pip install -e ./vendor/AutoViz

# DeepEye APIs
if [ ! -d vendor/DeepEye/.git ]; then
	git clone https://github.com/Thanksyy/DeepEye-APIs.git vendor/DeepEye
fi

# run main script
python -m main
