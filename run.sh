#!/bin/bash

w=$(dirname $(readlink -f "$0"))

python3 $w/core/routes.py
