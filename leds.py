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

#start random blinking of leds
blink = False

# pixels.fill fills ALL pixels with the given color
# color with value (0,0,0) is black, i.e. no color

# sets the first led to color red
# pixels[0] = (255,0,0)


def init():
    testr()
    #blinker()


def testr():
    for i in range(0, 1):
        #rot
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(3)
    
        #gruen
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(3)

    #    # no fill
    #     pixels.fill((0, 0, 0))
    #     pixels.show()
    #     time.sleep(2)

        #blau    
        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(3)
    reset()

def reset():
    # set all pixels to no color
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

    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
            pixels.show()
        time.sleep(wait)
    reset()

def rotate_one_round(time_per_led):
    # rotate through all leds one whole circle/round, time per led in seconds
    color = wheel(random.randrange(0, 255))
    for i in range(len(pixels)):
        reset()
        pixels[i] = color
        pixels.show()
        time.sleep(time_per_led)
    reset()

def blinker():
    
    if blink:
        pixels.fill((0, 0, 0))
        pixels[random.randrange(len(pixels))] = wheel(random.randrange(0, 255))
        pixels.show()
    else:
        reset()

    threading.Timer(0.80, blinker).start()

def switch_all_on_with_color(color=None):
    switch_on_with_color(list(range(6)), color)

def switch_on_with_color(number, color=None):
    # single number from 0 to 5 or tuple(1,3,5); color like (0, 255, 0)
    reset()

    # random color if none given
    if color is None:
        color = wheel(random.randrange(0, 255))

    if isinstance(number, tuple):
        # leds.switch_on_with_color((0,3,5), (200,200,100))
        for c in number:
            pixels[c] = color
    
    elif isinstance(number, list):
        # expect players list
        for i, p in enumerate(number):
            if p is not None:
                pixels[i] = color
    else:
        pixels[number] = color
        
    pixels.show()