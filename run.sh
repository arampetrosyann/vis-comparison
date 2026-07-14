#!/bin/bash

source .venv/bin/activate
pip install -e '.[dev]'

# AutoViz
if [ ! -d vendor/AutoViz/.git ]; then
	git clone https://github.com/AutoViML/AutoViz.git vendor/AutoViz
fi

if [[ "${1}" == "autoviz" ]]; then
	pip install -e ./vendor/AutoViz
fi

# DeepEye APIs
if [ ! -d vendor/DeepEye/.git ]; then
	git clone https://github.com/Thanksyy/DeepEye-APIs.git vendor/DeepEye
fi

# Data2Vis
if [ ! -d vendor/data2vis/.git ]; then
	git clone https://github.com/victordibia/data2vis.git vendor/data2vis
fi

# LLM4Vis
if [ ! -d vendor/LLM4Vis/.git ]; then
    git clone https://github.com/demoleiwang/LLM4Vis.git vendor/LLM4Vis
fi

# Table2Charts
if [ ! -d vendor/Table2Charts/.git ]; then
    git clone https://github.com/microsoft/Table2Charts.git vendor/Table2Charts
fi

if [[ "${1}" == "llm4vis" ]]; then
	export OPENAI_API_KEY="" # set your OpenAI API key here
    export OPENAI_API_BASE="https://api.openai.com/v1"
fi

# run main script
python -m main "$@"
