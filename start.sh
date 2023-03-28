#!/bin/bash
echo "Starting IOGR API"
source variables.conf
pip install virtualenv
python -m virtualenv ./app/env
./app/env/bin/pip install -r ./app/requirements.txt
./app/env/bin/python ./app/application.py