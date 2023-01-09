#!/usr/bin/python3
# -*- coding: UTF8 -*-

# shutdown Raspberry Pi with button press

import audio
#import RPi.GPIO as GPIO
import digitalio
import board
import os
import time
import leds

print("starting switch off")

#gpio13 (pin 33) - status/trigger
#pin_nr = 13

off_btn = digitalio.DigitalInOut(board.D13)
off_btn.direction = digitalio.Direction.INPUT
off_btn.pull = digitalio.Pull.UP

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM) #gpio not pin nr
#GPIO.setup(pin_nr, GPIO.IN, pull_up_down=GPIO.PUD_UP)

start_pressed = 0
pressed = False

# push threshold (in seconds)
threshold_time = 3

while True:
	if not off_btn.value:
	#if (GPIO.input(pin_nr)) == GPIO.LOW:
		if pressed == False:
			start_pressed = time.time()
			pressed	= True
		if pressed == True:
			if start_pressed+threshold_time < time.time():
				print("shutdown")
				audio.play_full("TTS",3) #Tschüss ich schalte mich jetzt aus
				leds.reset()
				os.system("shutdown -P now")

	else:
		pressed = False
