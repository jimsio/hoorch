#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import pygame
import rfidreaders
import leds
import time
import copy
import os

hoerspiele = {}

def start():
    print("Wir spielen Hörspiele")

    #TODO Wir spielen Hörspiele ab
    #audio.play_full("TTS", xx)
    leds.reset()  # reset leds

    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(frequency=22050, buffer=512, channels=1)
        pygame.mixer.init()
        
        for hoerspiel in os.listdir("./data/hoerspiele/"):
            #make a dictionary with the name of the hoerspiel as Key, and the pygame Sound as Value
            hoerspiele[os.path.splitext(hoerspiel)[0]]=pygame.mixer.Sound("data/hoerspiele/"+hoerspiel)

    else:
        pygame.mixer.unpause()

    leds.blink = True

    currently_playing = None

    while True:
        tags_on_board = copy.deepcopy(rfidreaders.tags)

        #if nothing is playing
        if currently_playing is None:
            #play the first you find
            for tag in tags_on_board:
                if tag in hoerspiele:
                    hoerspiele[tag].play()
                    currently_playing = tag
                    break

        #if tag of currently played song is still on the board
        elif currently_playing in tags_on_board:
            continue
        
        #if tag was removed from board
        elif currently_playing not in tags_on_board:
            hoerspiele[currently_playing].stop()
            currently_playing = None

        if "ENDE" in tags_on_board:
            # pygame.mixer.stop()
            pygame.mixer.quit()
            #pygame.mixer.pause()
            break

        time.sleep(1)
    
    leds.blink = False
    leds.reset()

