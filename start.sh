#!/usr/bin/bash

export PYTHONPATH=$(pwd)/src:$PYTHONPATH
source .venv/bin/activate
sudo python src/Tree.py