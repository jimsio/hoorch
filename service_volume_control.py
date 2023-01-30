#!/usr/bin/python3
# -*- coding: UTF8 -*-

import os
import subprocess
from shlex import split
import board
import digitalio

print("starting adjust volume")

os.system("amixer -q -M sset PCM 80%")

vol_up_btn = digitalio.DigitalInOut(board.D2)
vol_up_btn.direction = digitalio.Direction.INPUT
vol_up_btn.pull = digitalio.Pull.UP

vol_down_btn = digitalio.DigitalInOut(board.D3)
vol_down_btn.direction = digitalio.Direction.INPUT
vol_down_btn.pull = digitalio.Pull.UP

# cmd = "amixer -c 0 sget 'Headphone',0"
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
        # os.system("amixer -q -c 0 sset 'Headphone',0 5db+")
        os.system("amixer -q sset PCM 10+")


def volume_down():
    print("volume down")
    # os.system("amixer -q -c 0 sset 'Headphone',0 5db-")
    os.system("amixer -q sset PCM 10-")

# GPIO.add_event_detect(vol_up_pin, GPIO.FALLING, callback=volume_up, bouncetime = 400)
# GPIO.add_event_detect(vol_down_pin, GPIO.FALLING, callback=volume_down, bouncetime = 400)


while True:
    # continue
    if not vol_up_btn.value:  # VOL UP
        volume_up()
    elif not vol_down_btn.value:  # VOL DOWN
        volume_down()
