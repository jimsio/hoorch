#!/usr/bin/env python3
# -*- coding: UTF8 -*-

# require: see installer.sh

import time
import os
import subprocess
import audio
import rfidreaders
import leds
import game_tierlaute
import game_geschichten_aufnehmen
import game_kakophonie
import game_tier_orchester
import game_geschichten_abspielen
import game_einmaleins
import game_animals_english
import admin
import tagwriter

def init():
    print("initializiation of hardware")

    # initialize audio
    audio.init()

    audio.play_full("TTS", 1)

    # initialize leds
    leds.init()

    # start random blinker
    leds.random_timer = True

    # initialize readers
    #rfidreaders.init()

    # initialize figure_db if no tags defined for this hoorch set
    if not os.path.exists("./figure_db.txt"):
        # tell the ip adress
        output = None
        while True:
            output = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')

            if output is None or output == '\n': 
                audio.espeaker("WeiFei nicht verbunden")
                time.sleep(1.00)
            
            else:
                break
    
        ip_adress = output.split(" ", 1)
        audio.espeaker(ip_adress[0])

        leds.random_timer = False
        initial_hardware_test()
        #tagwriter.write_set()

    # start random blinker
    leds.random_timer = True


def initial_hardware_test():
    # test run to check hardware on first hoorch start - will test leds, readers, speakers, microphone
    leds.random_timer = False

    audio.espeaker("Jetzt wird die ganze Hardware getestet")

    audio.espeaker("Jetzt werden alle LEDs beleuchtet.")
    #leds.rainbow_cycle(0.001)
    leds.rainbow_cycle(0.01)

    # audio.espeaker("Wir testen jetzt die Ar ef eidi Leser.")
    # for i in range(6):
    #     audio.espeaker("Lege eine Karte auf Leser {0}".format(i+1))
    #     leds.switch_on_with_color(i, (255, 0, 0))
    #     while True:
    #         if rfidreaders.tags[i] is not None:
    #             break
    #     leds.reset()

    audio.espeaker(
        "Ich teste jetzt das Audio, die Aufnahme beginnt in 3 Sekunden und dauert 6 Sekunden")
    #leds.rotate_one_round(0.5)
    time.sleep(3)
    #subprocess.Popen("AUDIODEV=dmic_sv rec -c 1 ./data/figures/test/test.mp3", shell=True, stdout=None, stderr=None, timeout=6)
    audio.record_story("test")
    print("recording started und sleep 6")
    audio.espeaker("Jetzt werden alle LEDs beleuchtet.")
    #time.sleep(6)
    #leds.rotate_one_round(1)
    print("fertig mit sleep")
    error = audio.stop_recording("test")
    leds.reset()

    audio.espeaker("Ich spiele dir jetzt die Geschichte vor")
    audio.play_story("test")
    time.sleep(7)

    audio.espeaker("Test erfolgreich abgeschlossen.")


def main():
    print("start main loop")
    shutdown_time = 300  # seconds until shutdown if no interaction happened
    shutdown_counter = time.time()+shutdown_time

    greet_time = time.time()

    while True:
        # while shutdown_counter > time.time():

        leds.random_timer = True

        if greet_time < time.time():
            audio.play_full("TTS", 2)  # Welches Spiel wollt ihr spielen?
            greet_time = time.time()+30

        # Erklärung
        if "FRAGEZEICHEN" in rfidreaders.tags:
            print("Hoorch Erklärung")
            leds.random_timer = False
            audio.play_full("TTS", 65)  # Erklärung
            shutdown_counter = time.time()+shutdown_time

        # Games
        if "Aufnehmen" in rfidreaders.tags:
            print("Geschichten aufnehmen")
            leds.random_timer = False
            game_geschichten_aufnehmen.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu
            shutdown_counter = time.time()+shutdown_time

        if "Abspielen" in rfidreaders.tags:
            print("Geschichte abspielen")
            leds.random_timer = False
            game_geschichten_abspielen.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Tierlaute" in rfidreaders.tags:
            print("Tierlaute erkennen")
            leds.random_timer = False
            game_tierlaute.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "TierOrchester" in rfidreaders.tags:
            print("Tier-Orchester")
            leds.random_timer = False
            game_tier_orchester.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Kakophonie" in rfidreaders.tags:
            print("Kakophonie")
            leds.random_timer = False
            game_kakophonie.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Einmaleins" in rfidreaders.tags:
            print("Einmaleins")
            leds.random_timer = False
            game_einmaleins.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Animals" in rfidreaders.tags:
            print("Animals")
            leds.random_timer = False
            game_animals_english.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        # NFC tools on Android: write text to tag: ADMIN#
        if "ADMIN" in rfidreaders.tags:
            admin.main()
            shutdown_counter = time.time()+shutdown_time

        time.sleep(0.3)

    # shutdown
    print("shutdown")
    # Du hast mich lange nicht verwendet. Ich schalte mich zum Stromsparen jetzt aus.
    audio.play_full("TTS", 196)
    leds.random_timer = False
    leds.led_value = [1, 1, 1, 1, 1, 1]
    # os.system("shutdown -P now")


if __name__ == "__main__":
    init()
    main()
