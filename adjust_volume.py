#!/usr/bin/python3
# -*- coding: UTF8 -*-

import RPi.GPIO as GPIO
import os
import subprocess
from shlex import split

print("starting adjust volume")

#set start value of audio output
os.system("amixer -q -c 0 sset 'Headphone',0 82%") #=48 in alsamixer
#os.system("amixer -q -c 0 sset 'Headphone',0 86%") #=56 in alsamixer

vol_up_pin = 36 # volume up
vol_down_pin = 38 # volume down

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(vol_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vol_down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cmd = "amixer -c 0 sget 'Headphone',0"
cmd = split(cmd)

def volume_up(pin):
	get_volume = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
	position = get_volume.find("%")
	cv = int(get_volume[position-2:position].replace("[", ""))
	print(cv)

	if cv <= 82:
	#if cv <= 85:
		print("volume up")
		os.system("amixer -q -c 0 sset 'Headphone',0 5db+")

def volume_down(pin):
	print("volume down")
	os.system("amixer -q -c 0 sset 'Headphone',0 5db-")

GPIO.add_event_detect(vol_up_pin, GPIO.FALLING, callback=volume_up, bouncetime = 400)
GPIO.add_event_detect(vol_down_pin, GPIO.FALLING, callback=volume_down, bouncetime = 400)

while True:
	continue
