#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import threading
import RPi.GPIO as GPIO
import time
import random

#LEDS

#todo GPIO.setwarnings(False)
#todo GPIO.setmode(GPIO.BOARD)

#led_pins = [board.D23, board.D18, board.D17, board.D12, board.D7, board.D8]
#TODO: use BOARD numbers
led_pins = [23,18,17,12,7,8]#= GPIO pins (BCM)
led = []
led_value = [0,0,0,0,0,0]

rotate_timer = None
random_timer = False


def init():
	global led
	for led_pin in led_pins:
		GPIO.setup(led_pin,GPIO.OUT)
		#l = GPIO.PWM(led_pin,100)
		#l.start(100)
		#led.append(l)
	check_status()
	randomer()

def reset():
	global led_value
	led_value = [0,0,0,0,0,0]

def check_status():
	leds_timer = threading.Timer(0.01,check_status).start()
	for i in range(0,6):
		GPIO.output(led_pins[i], led_value[i])
	
#rotate through all leds one whole circle/round, time per led in seconds
def rotate_one_round(time_per_led):
	global led_value
	for i in range(0,6):
		reset()
		led_value[i] = 1
		time.sleep(time_per_led)
		reset()


#not used
#TODO : implement as threaded timer - so it can be stopped 
def rotate_timer(time_until_end, start_position):
	time_per_led = time_until_end / 6
	global led_value
	led_value = [1,1,1,1,1,1]
	
	for x in range(0,5):
		position = start_position+x
		if position > 5:
			position -= 5
		led_value[x] = 0
		time.sleep(time_per_led)
	

#rotate leds
rotate_led = 0
#not used
def rotate():
	global rotate_led
	global rotate_timer
	rotate_timer = threading.Timer(0.2,rotate).start()
	for index,i in enumerate(led_value):
		if index is rotate_led:
			led_value[index] = 1
		else: 
			led_value[index] = 0
	rotate_led += 1
	if rotate_led > 5:
		rotate_led = 0


def randomer():
	global random_timer
	threading.Timer(0.25,randomer).start()
	if random_timer:
		for index,i in enumerate(led_value):
			led_value[index] = random.randint(0,1)
