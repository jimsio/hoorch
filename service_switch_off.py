#!/usr/bin/python3
# -*- coding: UTF8 -*-

# shutdown Raspberry Pi with button press

import os
import time
import digitalio
import board
from adafruit_debouncer import Debouncer
import audio
import leds
import time

print("starting switch off")

off_btn = digitalio.DigitalInOut(board.D13)
off_btn.direction = digitalio.Direction.INPUT
off_btn.pull = digitalio.Pull.UP

off = Debouncer(off_btn, interval=0.05)

# push threshold (in seconds)
threshold_time = 3

while True:
    off.update()

    if off.rose:
        #if button is released, check if it was pressed for at least 3 seconds
        if off.last_duration > threshold_time:
            print("shutdown")
            leds.blink = False
            time.sleep(0.5)
            leds.reset()
            leds.switch_all_on_with_color((255,0,0))
            audio.play_full("TTS", 3)  # Tschüss ich schalte mich jetzt aus
            os.system("shutdown -P now")
        
    time.sleep(1)