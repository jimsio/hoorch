#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import os
import time
import random
import copy
import audio
import rfidreaders
import leds

defined_figures = rfidreaders.gamer_figures
defined_animals = rfidreaders.animal_figures


def start():
    animals_played = []  # store the already played animals to avoid repetition

    audio.play_full("TTS", 192)  # Wir lernen jetzt Tiernamen auf Englisch.
    leds.reset()  # reset leds

    if "ENDE" in rfidreaders.tags:
        return

    # Wenn ihr die Tiernamen auf Englisch lernen wollt, stellt die Fragezeichenfigur auf ein Spielfeld. Wenn ihr sie in einem Spiel erraten wollt, stellt eure Spielfiguren auf die Spielfelder.
    audio.play_full("TTS", 193)

    if "ENDE" in rfidreaders.tags:
        return

    audio.play_file("sounds", "waiting.mp3")  # play wait sound
    leds.rotate_one_round(1.11)

    # check for figures on board, filter other tags
    players = copy.deepcopy(rfidreaders.tags)

    isthefirst = True

    if "ENDE" in rfidreaders.tags:
        return

    # learn english names of animals
    if "FRAGEZEICHEN" in players:
        audio.play_full("TTS", 192)
        # Stelle einen Tier-Spielstein auf ein Spielfeld, ich sage dir dann den englischen Namen.
        audio.play_full("TTS", 195)
        while True:
            figures_on_board = copy.deepcopy(rfidreaders.tags)
            if "ENDE" in figures_on_board:
                leds.random_timer = False
                leds.reset()
                audio.kill_sounds()
                break

            for i, animal in enumerate(figures_on_board):
                if animal is not None:
                    animal = animal[:-1]  # remove digit at end
                    if animal in defined_animals:
                        leds.switch_on_with_color(i)
                        if not audio.file_is_playing(animal+".mp3"):
                            audio.play_file("TTS/animals_en", animal+".mp3")
                            time.sleep(2)
                        leds.reset()

    # play guessing game
    else:
        for i, p in enumerate(players):
            if p not in defined_figures:
                players[i] = None

        figure_count = sum(x is not None for x in players)

        time.sleep(1)
        if figure_count == 0:
            # Du hast keine Spielfigure auf das Spielfeld gestellt.
            audio.play_full("TTS", 59)
            return

        audio.play_full("TTS", 5+figure_count)  # Es spielen x Figuren mit

        rounds = 3  # 1-5 rounds possible
        audio.play_full("TTS", 20+rounds)  # Wir spielen 1-5 Runden
        points = [0, 0, 0, 0, 0, 0]

        for r in range(0, rounds):
            # print(players)
            for i, p in enumerate(players):
                if p is not None:
                    leds.reset()
                    leds.switch_on_with_color(i)
                    # led_value[i] = 100

                    if r == 0 and isthefirst == True:  # first round
                        isthefirst = False
                        if figure_count > 1:
                            # Es beginnt die Spielfigur auf Spielfeld x
                            audio.play_full("TTS", 12+i)
                        # Ich spiele dir jetzt die englischen Namen eines Tiers vor. Wenn du das Tier weisst, tausche deine Spielfigur gegen den Tier-Spielstein aus.
                        audio.play_full("TTS", 194)
                    elif figure_count == 1:
                        audio.play_full("TTS", 67)  # Du bist nochmal dran
                    else:
                        # Die nächste Spielfigur steht auf Spielfeld x
                        audio.play_full("TTS", 48+i)

                    # 20 different animals, up to 6 players, up to 5 rounds, need to empty animals_played when 20 reached
                    if len(animals_played) == 20:
                        animals_played = animals_played[-1]
                    # very first round, add dummy animal
                    elif len(animals_played) == 0:
                        animals_played.append("dummy_animal")

                    animal = random.choice(defined_animals)
                    while animal in animals_played:
                        animal = random.choice(defined_animals)

                    audio.play_file("TTS/animals_en", animal+".mp3")
                    time.sleep(2)

                    if "ENDE" in rfidreaders.tags:
                        return

                    while True:
                        if "ENDE" in rfidreaders.tags:
                            return

                        if not audio.file_is_playing(animal+".mp3"):
                            audio.play_file("TTS/animals_en", animal+".mp3")
                            time.sleep(3)

                        figure_on_field = copy.deepcopy(rfidreaders.tags[i])

                        if figure_on_field is not None:
                            # remove digit at end
                            figure_on_field = figure_on_field[:-1]

                            # avoid player figure, last animal (if remained on field) and any other figure than animals
                            if figure_on_field != p and figure_on_field != animals_played[-1] and figure_on_field in defined_animals:
                                audio.kill_sounds()

                                if figure_on_field == animal:
                                    time.sleep(0.2)
                                    audio.play_full("TTS", 27)
                                    print("richtig")
                                    audio.play_file("sounds", "winner.mp3")
                                    time.sleep(0.2)
                                    points[i] += 1
                                    print("Du hast schon " +
                                          str(points[i])+" richtige Antworten")
                                    rfidreaders.tags[i] = None
                                    break
                                else:
                                    time.sleep(0.2)
                                    audio.play_full("TTS", 26)
                                    print("falsch")
                                    audio.play_file("sounds", "loser.mp3")
                                    time.sleep(0.2)
                                    rfidreaders.tags[i] = None
                                    break

                    # add the current animal to the already played list
                    animals_played.append(animal)

    if not isthefirst:

        # tell the points
        audio.play_full("TTS", 80)  # Ich verlese jetzt die Punkte
        for i, p in enumerate(players):
            if p is not None:
                leds.reset()
                leds.led_value[i] = 100
                # Spielfigur auf Spielfeld 1,2...6
                audio.play_full("TTS", 74+i)
                time.sleep(0.2)
                print("Du hast "+str(points[i])+" Antworten richtig")
                audio.play_full("TTS", 68+points[i])
                time.sleep(1)

    leds.reset()
