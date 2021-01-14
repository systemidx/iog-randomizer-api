#!/bin/bash
echo "Starting IOGR API"
source /var/lib/iogr/variables.conf \
&& pip3 install virtualenv \
&& python3 -m virtualenv /var/lib/iogr/env \
&& sudo /var/lib/iogr/env/bin/pip install -r /var/lib/iogr/requirements.txt \
&& /var/lib/iogr/env/bin/python /var/lib/iogr/application.py