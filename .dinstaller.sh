#!/bin/bash

clear

sudo apt install python3-pip
pip install selenium

clear

echo "What do you want to search?"

read search

python3 main.py -s $search
