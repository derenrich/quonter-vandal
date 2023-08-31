#!/bin/bash

# run this after doing
# webservice --backend=kubernetes python3.11 shell

source $HOME/www/python/venv/bin/activate
cd ~/quonter-vandal
poetry export --without-hashes -f requirements.txt -o requirements.txt
pip install --no-cache-dir -r requirements.txt
pip install ~/quonter-vandal
