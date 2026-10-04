#!/bin/bash
echo "Starting IOGR API"
if [ -f variables.conf ]; then
    source variables.conf
fi

if [ ! -d "env" ] && [ -z "$VIRTUAL_ENV" ]; then
    python3 -m venv env
    ./env/bin/pip install -r requirements.txt
fi

if [ -f "./env/bin/python" ]; then
    exec ./env/bin/python application.py
else
    exec python3 application.py
fi