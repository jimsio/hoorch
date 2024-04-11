#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import os
import time
import subprocess
import rfidreaders
import leds
import audio

def start(figure_id):
    leds.reset()  # reset leds

    field = rfidreaders.tags.index(figure_id)
    
    #switch on led where tag is placed
    leds.switch_on_with_color(field, (0, 255, 0))

    error_recording = False
    figure_folder = "./data/figures/"
    figure_dirs = os.listdir(figure_folder)
    figure_dir = figure_folder+figure_id
    
    if figure_id not in figure_dirs:
        os.mkdir(figure_dir)

    audio.play_full("TTS", 56)  # Die Aufnahme beginnt in 3 Sekunden! Wenn du fertig bist, nimm deine Spielfigur vom Spielfeld"
    audio.play_full("TTS", 66)  # 3 2 1 Los
    leds.switch_on_with_color(field, (255, 0, 0))

    audio.record_story(figure_id)

    record_timer = time.time()+600  # 600 sec (=10min) counter until stop
    while True:
        if rfidreaders.tags[field] is None or record_timer < time.time() or "ENDE" in rfidreaders.tags:
            error_recording = audio.stop_recording(figure_id)
            audio.play_full("TTS", 57)  # Aufnahme ist zu Ende"

            break


    if error_recording:
        print("error while recording!")
        # Bei der Aufname ist ein Fehler passiert. Lass die Figur beim nächsten mal länger stehen
        audio.play_full("TTS", 197)
        return

    # play audio after recording
    # Ich spiele dir jetzt die Aufnahme vor. Verwende zum Speichern den Ja-Spielstein. Zum Verwerfen den Nein-Spielstein
    audio.play_full("TTS", 81)

    audio.play_story(figure_id)

    # wait 60 seconds longer than recording - prevent program from freezing
    waitingtime = time.time() + float(subprocess.run(
        ['soxi', '-D', figure_dir+'/'+figure_id+'.mp3'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8'))+60

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
                # never delete the folder
                #os.rmdir(figure_dir)
            else:
                # delete file
                os.remove(figure_dir+"/"+figure_id+".mp3")
                # rename second file in folder to figure_id without timestamp
                os.rename(
                    figure_dir+"/"+sorted_files[-1], figure_dir+"/"+figure_id+".mp3")

            # Geschichte nicht gespeichert
            audio.play_full("TTS", 83)
            break
    
    leds.reset()