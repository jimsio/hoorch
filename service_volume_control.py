#!/usr/bin/python3
# -*- coding: UTF8 -*-

import os
import subprocess
from shlex import split
import board
import digitalio
from adafruit_debouncer import Debouncer

print("starting adjust volume")

os.system("amixer -q -M sset PCM 80%")

vol_up_btn = digitalio.DigitalInOut(board.D2)
vol_up_btn.direction = digitalio.Direction.INPUT
vol_up_btn.pull = digitalio.Pull.UP

vol_down_btn = digitalio.DigitalInOut(board.D3)
vol_down_btn.direction = digitalio.Direction.INPUT
vol_down_btn.pull = digitalio.Pull.UP

vol_up = Debouncer(vol_up_btn, interval=0.05)
vol_down = Debouncer(vol_down_btn, interval=0.05)

cmd = "amixer sget PCM"
cmd = split(cmd)


def volume_up():
    get_volume = subprocess.run(
        cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    position = get_volume.find("%")
    cv = int(get_volume[position-2:position].replace("[", ""))
    print(cv)

    if cv <= 95:
        print("volume up")
        os.system("amixer -q sset PCM 10+")


def volume_down():
    print("volume down")
    os.system("amixer -q sset PCM 10-")

while True:
    vol_up.update()
    vol_down.update()

    if vol_up.fell:
        #volume up button pressed
        volume_up()
    elif vol_down.fell:
        #volume down button pressed
        volume_down()
