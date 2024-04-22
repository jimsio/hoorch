#!/usr/bin/env python3
# -*- coding: UTF8 -*-
import time
import os
import subprocess
import datetime
import re
import dbus
import rfidreaders
import audio


def main():

    breaker = False

    # 2 minutes until exit if no user interaction occurs
    admin_exit_counter = time.time() + 120

    audio.espeaker("Sie befinden sich im Admin-Menü.")

    subprocess.run(['git', 'remote', 'update'], stdout=subprocess.PIPE, check=False)
    #suche nach behind - subprocess outputs something like this if not up to date: "Your branch is behind 'origin/master' by 1 commit..."
    git_status = subprocess.run(['git', 'status', '-uno'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')
    if "behind" in git_status:
        audio.espeaker("Es ist ein Update verfügbar")

    audio.espeaker(
        "Verwenden Sie die Zahlenkarten um Einstellungen vorzunehmen.")
    audio.espeaker("1 - Software aktualisieren.")
    audio.espeaker("2 - WeiFei-Konfiguration.")
    audio.espeaker("3 - Spielfiguren-Set löschen.")
    audio.espeaker("4 - Alle Geschichten archivieren")
    audio.espeaker("Ende-Täg zum Beenden.")

    while admin_exit_counter > time.time():

        for tag_name in rfidreaders.tags:
            if tag_name is not None and re.search("^[A-z]*[0-9]$", tag_name):
                op = int(tag_name[-1])  # 1 from Hahn1

                if op == 1:
                    # git update
                    git()
                    admin_exit_counter = time.time() + 120
                elif op == 2:
                    wifi()
                    admin_exit_counter = time.time() + 120
                elif op == 3:
                    # delete figure_db.txt, restart hoorch
                    new_set()

                elif op == 4:
                    # archive all figure stories
                    archive_stories()
                    admin_exit_counter = time.time() + 120
            elif tag_name == "ENDE":
                breaker = True
                break

        if breaker:
            break

    audio.espeaker("Admin-Menü beendet.")


def archive_stories():
    figure_dir = "./data/figures/"
    print("archive stories")
    recordings_list = os.listdir(figure_dir)

    for folder in recordings_list:
        if os.path.isdir(figure_dir+folder):
            if folder+".mp3" in os.listdir(figure_dir+folder+"/"):
                now = datetime.datetime.now()
                os.rename(f"{figure_dir}{folder}/{folder}.mp3", f"{figure_dir}{folder}/{folder}-{now:%Y-%m-%d-%H-%M}.mp3")
                print(folder+".mp3 put into archive")

            else:
                print(folder + "-stories already in archive")

    audio.espeaker("Alle Geschichten wurden archiviert.")


def new_set():
    print("delete figure_db.txt, restart hoorch")
    os.rename("figure_db.txt", "figure_db-{0}.txt".format(
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
    audio.espeaker("Figuren-Datenbank gelöscht. Ich starte jetzt neu.")
    os.system("reboot")


def git():
    print("git update, restart hoorch")
    bus = dbus.SystemBus()
    # get comitup dbus object - https://davesteele.github.io/comitup/man/comitup.8.html
    nm = bus.get_object('com.github.davesteele.comitup',
                        '/com/github/davesteele/comitup')

    tpl = nm.state()

    # state is either 'HOTSPOT', 'CONNECTING', or 'CONNECTED'
    state = str(tpl[0])

    if state == "HOTSPOT":
        audio.espeaker("Weifei nicht verbunden.")
        audio.espeaker(
            "Öffne zuerst mit der Zahlenkarte 1 die WeiFei Konfiguration.")

    elif state == "CONNECTED":
        audio.espeaker(
            "Aktualisierung wird gestartet. Dies kann einige Minuten dauern. Hoorch startet anschließend neu.")
        # Any local files that are not tracked by Git will not be affected:
        # git fetch downloads the latest from remote without trying to merge or rebase anything.
        # git reset resets the master branch to what you just fetched. 
        # The --hard option changes all the files in your working tree to match the files in origin/master.
        subprocess.run(['git', 'fetch', '--all'], stdout=subprocess.PIPE, check=False)
        #subprocess.run(['git', 'branch', 'backup-master'], stdout=subprocess.PIPE)
        subprocess.run(['git', 'reset', '--hard', 'origin/master'], stdout=subprocess.PIPE, check=False)

        audio.espeaker("Aktualisierung beendet. Ich starte jetzt neu.")
        os.system("reboot")


def wifi():
    print("wifi config")
    rfkill_output = subprocess.run(
        ['rfkill', 'list', 'wifi'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')

    if "yes" in rfkill_output:
        # wifi blocked / off
        audio.espeaker("Weifei ist ausgeschaltet.")
        audio.espeaker("Soll ich es einschalten?")

        while True:
            if "JA" in rfidreaders.tags:
                audio.espeaker(
                    "Weifei wird gestartet. Dies kann einen Augenblick dauern.")
                os.system("rfkill unblock wifi")

                while not subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8'):
                    time.sleep(2)

                output = subprocess.run(
                    ['hostname', '-I'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')
                ip_adress = output.split(" ", 1)
                print(ip_adress)

                audio.espeaker("Weifei eingeschaltet.")
                audio.espeaker("Die IP-Adresse lautet")
                audio.espeaker(ip_adress[0])

                break

            elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
                break
    else:
    # wifi on

        bus = dbus.SystemBus()
        # get comitup dbus object - https://davesteele.github.io/comitup/man/comitup.8.html
        nm = bus.get_object('com.github.davesteele.comitup',
                            '/com/github/davesteele/comitup')

        tpl = nm.state()

        # state is either 'HOTSPOT', 'CONNECTING', or 'CONNECTED'
        state = str(tpl[0])

        # connection - ssid name for the current connection on the wifi device
        connection = tpl[1]

        # accesspoint hostname
        info = nm.get_info()
        hostname = str(info["apname"])

        if state == "HOTSPOT":
            audio.espeaker("Keine Verbindung zum Internet.")
            audio.espeaker(
                f"Verbinde dich am Handy mit dem Hotspot namens {hostname}. Öffne dann im Brauser {hostname} Punkt local")
            audio.espeaker("Stelle dort dein lokales WeLan und Passwort ein")

        # connected to a wifi
        elif state == "CONNECTED":
            audio.espeaker(f"Mit WeiFei {connection} verbunden.")
            output = subprocess.run(
                ['hostname', '-I'], stdout=subprocess.PIPE, check=False).stdout.decode('utf-8')
            ip_adress = output.split(" ", 1)
            print(ip_adress)

            # say adress twice
            for i in range(2):
                audio.espeaker("Die IP-Adresse lautet")
                audio.espeaker(ip_adress[0])
            time.sleep(2)

            audio.espeaker("Soll ich es ausschalten?")

            while True:
                if "JA" in rfidreaders.tags:
                    # os.system("rfkill block wifi")
                    audio.espeaker("Weifei wurde gestoppt")
                    break

                elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
                    break

        # connecting
        else:
            audio.espeaker(
                "Internet in wenigen Augenblicken verfügbar. Bitte warten.")
            time.sleep(2)

    audio.espeaker("WeiFei-Konfiguration beendet.")
