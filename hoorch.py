#!/usr/bin/env python3
# -*- coding: UTF8 -*-

# require: see installer.sh
import os
import time
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
import game_hoerspiele
import game_aufnehmen
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
    #leds.blink = True

    # initialize readers
    rfidreaders.init()
    
    # initialize figure_db if no tags defined for this hoorch set
    if not os.path.exists("./figure_db.txt"):
        # tell the ip adress
        output = None
        while True:
            output = subprocess.run(
                ['hostname', '-I'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')

            if output is None or output == '\n':
                audio.espeaker("WeiFei nicht verbunden")
                time.sleep(1.00)
                #if connected to router but internet on router is down, we need to open 
                # comitup-cli and and delete connection with d and establish a new one

            else:
                break

        ip_adress = output.split(" ", 1)
        audio.espeaker("Die eipi Adresse lautet")
        audio.espeaker(ip_adress[0])

        initial_hardware_test()

        rfidreaders.read_continuously = False
        time.sleep(1)
        tagwriter.write_set()
        rfidreaders.read_continuously = True
        rfidreaders.continuous_read()


def initial_hardware_test():
    # test run to check hardware on first hoorch start - will test leds, readers, speakers, microphone
    #leds.blink = False

    audio.espeaker("Jetzt wird die ganze Hardware getestet")

    audio.espeaker("Jetzt werden alle LEDs beleuchtet.")
    ## leds.rainbow_cycle(0.001)
    leds.rainbow_cycle(0.01)

    audio.espeaker("Wir testen jetzt die Ar ef eidi Leser.")
    for i in range(6):
        leds.switch_on_with_color(i, (255, 0, 0))
        audio.espeaker(f"Lege eine Karte auf Leser {i+1}")
        while True:
            if rfidreaders.tags[i] is not None:
                break

    leds.reset()

    audio.espeaker(
        "Ich teste jetzt das Audio, die Aufnahme beginnt in 3 Sekunden und dauert 6 Sekunden")
    time.sleep(3)
    leds.switch_all_on_with_color()
    
    # switch off speakers to avoid clicking
    audio.amp_sd.value = False

    print("aufnahme starten")
    subprocess.Popen("AUDIODEV=dmic_sv rec -c 1 ./data/figures/test/test.aif",
                     shell=True, stdout=None, stderr=None)
    time.sleep(6)
    #leds.rotate_one_round(6)
    print("aufnahme beendet")
    subprocess.Popen("killall rec", shell=True, stdout=None, stderr=None)

    leds.reset()

    # switch on speakers
    audio.amp_sd.value = True

    if os.path.exists("./data/figures/test/test.aif"):
        audio.espeaker("Ich spiele dir jetzt die Geschichte vor")
        leds.switch_all_on_with_color()
        audio.play_file("figures/test", "test.aif")
        time.sleep(7)
        leds.reset()
    else:
        audio.espeaker("Aufnahme hat nicht geklappt. Audio nicht gefunden")

    audio.espeaker("Test abgeschlossen.")


def main():
    print("start main loop")
    shutdown_time = 300  # seconds until shutdown if no interaction happened
    shutdown_counter = time.time()+shutdown_time

    greet_time = time.time()

    while True:
    #while shutdown_counter > time.time():

        leds.blink = True

        if greet_time < time.time():
            audio.play_full("TTS", 2)  # Welches Spiel wollt ihr spielen?
            greet_time = time.time()+30

        # Erklärung
        if "FRAGEZEICHEN" in rfidreaders.tags:
            print("Hoorch Erklärung")
            leds.blink = False
            audio.play_full("TTS", 65)  # Erklärung
            shutdown_counter = time.time()+shutdown_time

        # Games
        if "Aufnehmen" in rfidreaders.tags:
            print("Geschichten aufnehmen")
            leds.blink = False
            game_geschichten_aufnehmen.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu
            shutdown_counter = time.time()+shutdown_time

        if "Abspielen" in rfidreaders.tags:
            print("Geschichte abspielen")
            leds.blink = False
            game_geschichten_abspielen.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Tierlaute" in rfidreaders.tags:
            print("Tierlaute erkennen")
            leds.blink = False
            game_tierlaute.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "TierOrchester" in rfidreaders.tags:
            print("Tier-Orchester")
            leds.blink = False
            game_tier_orchester.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Kakophonie" in rfidreaders.tags:
            print("Kakophonie")
            leds.blink = False
            game_kakophonie.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Einmaleins" in rfidreaders.tags:
            print("Einmaleins")
            leds.blink = False
            game_einmaleins.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time

        if "Animals" in rfidreaders.tags:
            print("Animals")
            leds.blink = False
            game_animals_english.start()
            audio.play_full("TTS", 54)  # Das Spiel ist zu Ende
            shutdown_counter = time.time()+shutdown_time
       
        #list of available hoerspiele without file extension - i.e. ['mutigTR', 'mutigDE', 'mutigHR']
        hoerspiele_list = [os.path.splitext(h)[0] for h in os.listdir("./data/hoerspiele/")]
        detected_hoerspiel_card = [i for i in hoerspiele_list if i in rfidreaders.tags]
          
        if detected_hoerspiel_card:
            print("Hoerspiele")
            leds.blink = False
            game_hoerspiele.start(f"hoerspiele/{detected_hoerspiel_card[0]}", detected_hoerspiel_card[0])
            shutdown_counter = time.time()+shutdown_time
       
        figure_dir = "./data/figures/"
        #get only folders, not files
        figure_dirs = [name for name in os.listdir(figure_dir) if os.path.isdir(os.path.join(figure_dir, name))]
        #list of available figures with a recording
        figure_with_recording = [k for k in figure_dirs if f"{k}.mp3" in os.listdir(figure_dir+k)]
        detected_figure_with_recording = [j for j in figure_with_recording if j in rfidreaders.tags]

        #all defined figure minus the ones with a recording
        defined_figures = rfidreaders.gamer_figures
        detected_figure_without_recording = [i for i in defined_figures if i not in figure_with_recording]

        #prioritize figures with recordings over the ones without
        if detected_figure_with_recording:
            print("Geschichte abspielen - from main menu")
            leds.blink = False
            #pick first figure detected
            game_hoerspiele.start(f"figures/{detected_figure_with_recording[0]}", detected_figure_with_recording[0])
            shutdown_counter = time.time()+shutdown_time
        

        elif detected_figure_without_recording:
            print("Geschichte aufnehmen - from main menu")
            leds.blink = False
            game_aufnehmen.start(detected_figure_without_recording[0])
            shutdown_counter = time.time()+shutdown_time

        # if "JA" and "NEIN" chips detected enter admin menu
        if "JA" in rfidreaders.tags and "NEIN" in rfidreaders.tags:
            admin.main()
            shutdown_counter = time.time()+shutdown_time

        time.sleep(0.3)

    # shutdown
    print("shutdown")
    # Du hast mich lange nicht verwendet. Ich schalte mich zum Stromsparen jetzt aus.
    audio.play_full("TTS", 196)
    leds.blink = False
    leds.led_value = [1, 1, 1, 1, 1, 1]
    # os.system("shutdown -P now")


if __name__ == "__main__":
    init()
    