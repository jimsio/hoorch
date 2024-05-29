#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import re
import pygame
import audio
import rfidreaders
import leds

phones = []


def start():
    print("Wir spielen Kakophonie")

    volume = 0

    # Wir spielen Kakophonie. Stelle die Zahlen 1 bis 6 auf die Spielfelder!
    audio.play_full("TTS", 64)
    leds.reset()  # reset leds

    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(frequency=22050, buffer=512)
        pygame.mixer.init()
        # pygame.mixer.init(buffer=4096)
        pygame.mixer.set_num_channels(6)

        for s in range(0, 6):
            phones.append(pygame.mixer.Sound("data/phonie/00"+str(s+1)+".ogg"))
            phones[s].set_volume(0)
    else:
        pygame.mixer.unpause()

    for p in phones:
        p.play(loops=-1)
    leds.blink = True

    while True:
        found_digits = []
        for i, tag in enumerate(rfidreaders.tags):
            if tag is not None:
                if re.search("^[A-z]*[0-9]$", tag):
                    found_digits.append(tag[-1])  # get digit

        for i in range(0, 6):
            if str(i+1) not in found_digits:
                phones[i].set_volume(0)
            else:
                phones[i].set_volume(volume)

        if "ENDE" in rfidreaders.tags:
            # pygame.mixer.stop()
            # pygame.mixer.quit()
            pygame.mixer.pause()
            break
    
    leds.blink = False
    leds.reset()
