#!/usr/bin/env sh
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"
python tests/mains.py
exit $?