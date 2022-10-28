#!/bin/bash

#check if venv exists if it doesn't create it
#check if depend.txt exists if it doesn't end code
#enter venv and install deps
#export venv dep with pip freeze > depend.txts

venv="netvenv"
depFile="depend.txt"
cur_path=$(pwd)

if [ ! -d $cur_path/$venv ]; then
    echo "Creating venv " $cur_path/$venv
    python3 -m venv $cur_path/$venv
    if [ $? -ne 0 ]; then
        echo "Could not create venv at "$cur_path/$venv
        exit 0
    fi
fi

source $cur_path/$venv"/bin/activate"

if [ ! -f $cur_path/$depFile ]; then
    exit 0
else
    echo "Installing venv dependancies"
    pip install -r $cur_path/$depFile

    if [ $? -ne 0 ]; then
        echo "Could not install dependancies"
        echo "updating python and pip! "
        echo "Fix pip error and run script again :)"
        exit 0
    else
        echo "Done !!"
        exit 0
    fi
fi