#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import copy
import time
import audio
import rfidreaders
import leds

defined_animals = rfidreaders.animal_figures


def start():
    # print(defined_animals)
    # Es spielt das Tier Orchester. Stelle die Tierfiguren auf die Spielfelder!
    audio.play_full("TTS", 63)
    leds.reset()  # reset leds

    playing_animals = [None, None, None, None, None, None]
    leds.blink = True
    while True:
        animals = copy.deepcopy(rfidreaders.tags)
        if "ENDE" in animals:
            leds.blink = False
            leds.reset()
            audio.kill_sounds()
            break

        for i, animal in enumerate(animals):
            if animal is not None:
                animal = animal[:-1]
            if animal not in defined_animals:
                animal = None
            if animal is not None:
                # print(animal)
                if not audio.file_is_playing(animal+".mp3"):
                    audio.play_file("animal_sounds", animal+".mp3")
                    playing_animals[i] = animal

        time.sleep(0.2)
