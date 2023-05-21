#!/bin/bash

w=$(dirname $(readlink -f "$0"))

python3 $w/telegram_bot/telegram_bot.py 
