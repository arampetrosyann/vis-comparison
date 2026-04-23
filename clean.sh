#!/bin/bash

find outputs/* -not -name ".gitignore" -type f -delete
find outputs/* -type d -exec rm -rf {} +
