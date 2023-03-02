#!/usr/bin/python3
# -*- coding: UTF8 -*-

# shutdown Raspberry Pi with button press

import os
import time
import digitalio
import board
from adafruit_debouncer import Debouncer
#import audio
#import leds

print("starting switch off")

off_btn = digitalio.DigitalInOut(board.D13)
off_btn.direction = digitalio.Direction.INPUT
off_btn.pull = digitalio.Pull.UP

off = Debouncer(off_btn, interval=0.3)

#start_pressed = 0
#pressed = False

# push threshold (in seconds)
threshold_time = 3

while True:
    off.update()

    if off.rose:
        #if button is released, check if it was pressed for at least 3 seconds
        if off.last_duration > threshold_time:
            print("shutdown")
            #audio.play_full("TTS", 3)  # Tschüss ich schalte mich jetzt aus
            #os.system("shutdown -P now")

    # if not off_btn.value:
    #     if not pressed:
    #         start_pressed = time.time()
    #         pressed = True
    #     if pressed:
    #         if start_pressed+threshold_time < time.time():
    #             print("shutdown")
    #             audio.play_full("TTS", 3)  # Tschüss ich schalte mich jetzt aus
    #             leds.reset()
    #             os.system("shutdown -P now")

    # else:
    #     pressed = False
