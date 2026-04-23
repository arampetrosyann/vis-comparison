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

# KG4Vis
if [ ! -d vendor/KG4Vis/.git ]; then
	git clone https://github.com/KG4VIS/Knowledge-Graph-4-VIS-Recommendation.git vendor/KG4Vis
fi

# run main script
python -m main
