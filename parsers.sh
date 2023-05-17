#!/bin/bash

w=$(dirname $(readlink -f "$0"))

mkdir -p $w/data $w/logs

cd $w/parsers

time=$(date +'%Y-%m-%d-%H-%M-%S')

python3 ./rbc_finances_parser.py > $w/logs/rbc-finances-parser-${time} 2>&1 &
python3 ./cfo_parser.py > $w/logs/cfo-parser-${time} 2>&1 &
python3 ./klerk_parser.py > $w/logs/klerk-parser-${time} 2>&1 &
python3 ./consultant_parser.py > $w/logs/consultant-parser-${time} 2>&1 &
wait
