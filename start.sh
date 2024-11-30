#!/bin/bash
echo "Starting IOGR API"
source variables.conf
pip install virtualenv
python -m virtualenv /home/bryon/app/env
/home/bryon/app/env/bin/pip install -r /home/bryon/app/requirements.txt
/home/bryon/app/env/bin/python /home/bryon/app/application.py