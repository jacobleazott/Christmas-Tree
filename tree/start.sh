#!/bin/bash

export PYTHONPATH=$(pwd)/src:$PYTHONPATH
cd /home/pi/Christmas-Tree/tree/
sudo python src/Tree.py