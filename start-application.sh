#!/bin/bash

export PYTHONPATH="`pwd`/app":$PYTHONPATH
source ./venv/bin/activate
python ./app/api.py