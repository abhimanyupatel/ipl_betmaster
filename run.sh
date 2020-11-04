#!/bin/sh
nohup python3 main.py > ipl_bot.log 2>&1 &
echo $! > save_ipl_bot_pid.txt