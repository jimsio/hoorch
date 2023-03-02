#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import time
import random
import threading
import neopixel
import board

# LEDS

# Neopixel connected to GPIO12 / pin32
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 6

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.2, auto_write=False, pixel_order=ORDER)

random_timer = False

# pixels.fill fills ALL pixels with the given color
# color with value (0,0,0) is black, i.e. no color

# sets the first led to color red
# pixels[0] = (255,0,0)


def init():
    random_blinker()


def testr():
    global pixels

    for i in range(0, 2):
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(0.3)

        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(0.3)

        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(0.3)

        # no fill
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.6)

def reset():
    # set all pixels to no color
    global pixels
    pixels.fill((0, 0, 0))
    pixels.show()



def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    # is that a way to make color picking easier?
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(wait):
    # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    global pixels

    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
            pixels.show()
        time.sleep(wait)

def rotate_one_round(time_per_led):
    # rotate through all leds one whole circle/round, time per led in seconds
    global pixels
    for i in range(len(pixels)):
        reset()
        pixels[i] = (0, 255, 0)
        pixels.show()
        time.sleep(time_per_led)
    reset()


def random_blinker():
    global pixels

    threading.Timer(0.25, random_blinker).start()
    if random_timer:
        pixels[random.randrange(len(pixels))] = (random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))
        pixels.show()

def switch_on_with_color(number, color=None):
    # single number from 0 to 5 or tuple(1,3,5); color like (0, 255, 0)
    global pixels

    # random color if none given
    if color is None:
        color = wheel(random.randrange(0, 255))

    if isinstance(number, tuple):
        # leds.switch_on_with_color((0,3,5), (200,200,100))
        for c in number:
            pixels[c] = color
            pixels.show()

    elif isinstance(number, list):
        # expect players list
        for i, p in enumerate(number):
            if p is not None:
                pixels[i] = color
                pixels.show()
    else:
        pixels[number] = color
        pixels.show()

# GPIO.setmode(GPIO.BCM) #= GPIO number (BCM)
# GPIO.setwarnings(False)
#
# led_pins = [23,18,17,12,7,8]#= GPIO number (BCM)
# led = []
# led_value = [0,0,0,0,0,0]

# rotate_timer = None
# random_timer = False

# def init():
# 	global led
# 	for led_pin in led_pins:
# 		GPIO.setup(led_pin,GPIO.OUT)
# 		#l = GPIO.PWM(led_pin,100)
# 		#l.start(100)
# 		#led.append(l)
# 	check_status()
# 	randomer()
#
# def reset():
# 	global led_value
# 	led_value = [0,0,0,0,0,0]
#
# def check_status():
# 	leds_timer = threading.Timer(0.05,check_status).start()
# 	for i in range(0,6):
# 		GPIO.output(led_pins[i], led_value[i])
#
# rotate through all leds one whole circle/round, time per led in seconds
# def rotate_one_round(time_per_led):
# 	global led_value
# 	for i in range(0,6):
# 		reset()
# 		led_value[i] = 1
# 		time.sleep(time_per_led)
# 		reset()
#
# def randomer():
# 	global random_timer
# 	threading.Timer(0.25,randomer).start()
# 	if random_timer:
# 		for index,i in enumerate(led_value):
# 			led_value[index] = random.randint(0,1)
#
#
# #not used
# #TODO : implement as threaded timer - so it can be stopped
# def rotate_timer(time_until_end, start_position):
# 	time_per_led = time_until_end / 6
# 	global led_value
# 	led_value = [1,1,1,1,1,1]
#
# 	for x in range(0,5):
# 		position = start_position+x
# 		if position > 5:
# 			position -= 5
# 		led_value[x] = 0
# 		time.sleep(time_per_led)
#
# #not used
# #rotate leds
# rotate_led = 0
# def rotate():
# 	global rotate_led
# 	global rotate_timer
# 	rotate_timer = threading.Timer(0.2,rotate).start()
# 	for index,i in enumerate(led_value):
# 		if index is rotate_led:
# 			led_value[index] = 1
# 		else:
# 			led_value[index] = 0
# 	rotate_led += 1
# 	if rotate_led > 5:
# 		rotate_led = 0
