#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import os
import copy
import subprocess
import time
import datetime
import audio
import rfidreaders
import leds


defined_figures = rfidreaders.gamer_figures


def start():

    # Wir nehmen eine Geschichte für deine Figur auf
    audio.play_full("TTS", 55)
    print("Wir nehmen eine Geschichte für deine Figur auf")

    leds.reset()  # reset leds

    audio.play_full("TTS", 5)  # Stelle deine Figur auf eines der Spielfelder

    audio.play_file("sounds", "waiting.mp3")  # play wait sound
    leds.rotate_one_round(1.11)

    players = copy.deepcopy(rfidreaders.tags)
    # check if player tag is predefined in definded_tags xor is number (than it's an unknown tag)
    for i, p in enumerate(players):
        if p not in defined_figures:
            players[i] = None

    figure_count = sum(x is not None for x in players)
    if figure_count == 0:
        # "Du hast keine Spielfigure auf das Spielfeld gestellt."
        audio.play_full("TTS", 59)
        return

    time.sleep(0.5)

    # switch on leds at player field
    leds.switch_on_with_color(players, (100, 100, 100))

    audio.play_full("TTS", 5+figure_count)  # Es spielen x Figuren mit

    if "ENDE" in rfidreaders.tags:
        return

    first_round = True
    for i, figure_id in enumerate(players):
        leds.reset()
        if figure_id is not None:
            leds.switch_on_with_color(i, (0, 255, 0))

            new_recording = False
            error_recording = False

            if figure_count > 1:
                if first_round:  # at start
                    # Es beginnt die Spielfigur auf Spielfeld x
                    audio.play_full("TTS", 12+i)
                    first_round = False
                else:
                    # Die nächste Spielfigur steht auf Spielfeld x
                    audio.play_full("TTS", 47+i)

            if "ENDE" in rfidreaders.tags:
                return

            recordings_list = os.listdir("./data/figures/")
            figure_dir = "./data/figures/"+figure_id

            # when figure folder and i.e. roboter.mp3 exist
            if figure_id in recordings_list and figure_id+'.mp3' in os.listdir(figure_dir):

                # Diese Figur hat schon eine Geschichte gespeichert...
                audio.play_full("TTS", 84)
                # files = os.listdir(figure_dir)
                audio.play_story(figure_id)

                # wait 60 seconds longer than recording otherwise continue to next figure - prevent program from freezing
                waitingtime = time.time() + float(subprocess.run(
                    ['soxi', '-D', figure_dir+'/'+figure_id+'.mp3'], stdout=subprocess.PIPE).stdout.decode('utf-8'))+60

                while waitingtime > time.time():
                    if "JA" in rfidreaders.tags:
                        # if rfidreaders.tags[i] == "JA":
                        audio.kill_sounds()

                        # Stelle deine Figur wieder auf dein Spielfeld.
                        audio.play_full("TTS", 200)

                        # rename old story
                        archived_file = figure_id+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
                        os.rename(figure_dir+"/"+figure_id+".mp3",
                                  figure_dir+"/"+archived_file+".mp3")

                        # Die Aufnahme beginnt in 3 Sekunden! Wenn du fertig bist, nimm deine Spielfigur vom Spielfeld"
                        audio.play_full("TTS", 56)
                        # leds.rotate_one_round(0.4)
                        audio.play_full("TTS", 66)  # 3 2 1 Los
                        leds.switch_on_with_color(i, (0, 255, 0))

                        # most recent story has only figure_id as filename, record_story(figure_id)
                        audio.record_story(figure_id)

                        record_timer = time.time()+600  # 600 sekunden(60*10min) counter until stop
                        while True:
                            if rfidreaders.tags[i] is None or record_timer < time.time() or "ENDE" in rfidreaders.tags:
                                error_recording = audio.stop_recording(
                                    figure_id)
                                # Aufnahme ist zu Ende
                                audio.play_full("TTS", 57)
                                new_recording = True
                                break
                        break

                    # elif rfidreaders.tags[i] == "NEIN" or "ENDE" in rfidreaders.tags:
                    elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
                        audio.kill_sounds()
                        # new_recording = False
                        break

            else:
                print("no story recorded yet")

                if figure_id not in recordings_list:
                    os.mkdir(figure_dir)

                # Die Aufnahme beginnt in 3 Sekunden! Wenn du fertig bist, nimm deine Spielfigur vom Spielfeld"
                audio.play_full("TTS", 56)
                # leds.rotate_one_round(0.4)
                audio.play_full("TTS", 66)  # 3 2 1 Los
                # time.sleep(1)
                leds.switch_on_with_color(i, (255, 0, 0))

                # most recent story has only figure_id as filename, record_story(figure_id)
                audio.record_story(figure_id)

                record_timer = time.time()+600  # 600 sekunden(=10min) counter until stop
                while True:
                    if rfidreaders.tags[i] is None or record_timer < time.time() or "ENDE" in rfidreaders.tags:
                        error_recording = audio.stop_recording(figure_id)
                        audio.play_full("TTS", 57)  # Aufnahme ist zu Ende"
                        new_recording = True
                        break

            if new_recording:

                if error_recording:
                    print("error while recording!")
                    # Bei der Aufname ist ein Fehler passiert. Lass die Figur beim nächsten mal länger stehen
                    audio.play_full("TTS", 197)
                    continue

                # play audio after recording
                # Ich spiele dir jetzt die Aufnahme vor. Verwende zum Speichern den Ja-Spielstein. Zum Verwerfen den Nein-Spielstein
                audio.play_full("TTS", 81)

                audio.play_story(figure_id)

                # wait 60 seconds longer than recording otherwise continue to next figure - prevent program from freezing
                waitingtime = time.time() + float(subprocess.run(
                    ['soxi', '-D', figure_dir+'/'+figure_id+'.mp3'], stdout=subprocess.PIPE).stdout.decode('utf-8'))+60

                while waitingtime > time.time():
                    # if rfidreaders.tags[i] == "JA":
                    if "JA" in rfidreaders.tags:
                        audio.kill_sounds()
                        audio.play_full("TTS", 82)  # Geschichte gespeichert
                        break

                    elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
                        # elif rfidreaders.tags[i] == "NEIN" or "ENDE" in rfidreaders.tags:
                        audio.kill_sounds()

                        files_in_dir = os.listdir(figure_dir)
                        sorted_files = sorted(files_in_dir)
                        # print(sorted_files)

                        if len(files_in_dir) <= 1:
                            # delete file
                            os.remove(figure_dir+"/"+figure_id+".mp3")
                            # delete folder
                            os.rmdir(figure_dir)
                        else:
                            # delete file
                            os.remove(figure_dir+"/"+figure_id+".mp3")
                            # rename second file in folder to figure_id without timestamp
                            os.rename(
                                figure_dir+"/"+sorted_files[-1], figure_dir+"/"+figure_id+".mp3")

                        # Geschichte nicht gespeichert
                        audio.play_full("TTS", 83)
                        break
