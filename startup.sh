#!/bin/bash

ping -c 1 google.com -W 1 > /dev/null

while [[ $? -ne 0 ]]; do
    echo "Connection dead"
    sudo ifconfig eno1 down && sudo ifconfig eno1 up
    sudo dhclient -v eno1
    ping -c 1 discord.com -W 1 &> /dev/null
done

/usr/bin/python3 /home/schapin/Scripts/Discord_Bot/bot.py

