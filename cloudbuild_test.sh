#!/usr/bin/env sh
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"
LOGGING_LEVEL=30 coverage run tests/main.py
coverage xml -i
exit $?