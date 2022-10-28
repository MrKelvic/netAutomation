#!/bin/bash
venv="netvenv"
depFile="depend.txt"
cur_path=$(pwd)
echo "sourcing python from " $cur_path/$venv
source $cur_path/$venv"/bin/activate"
echo "Running test script"
python3 testfn.py