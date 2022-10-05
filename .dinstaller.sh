#!/bin/bash

sudo apt install python3-pip
pip install selenium

echo "What do you want to search?"

read search

python3 main.py -s $search