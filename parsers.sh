#!/bin/bash

pip3 install beautifulsoup4 requests datetime

cd parsers

python3 ./rbc_finances_parser.py &
python3 ./cfo_parser.py &
python3 ./klerk_parser.py &
python3 ./consultant_parser.py &&
wait