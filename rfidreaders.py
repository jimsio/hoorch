#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import time
import threading
import os
import unicodedata
import board
import busio
from adafruit_pn532.spi import PN532_SPI
import digitalio
from digitalio import DigitalInOut
import audio

# gpio belegung
# Reader 1: Pin18 - GPIO24
# Reader 2: Pin15 - GPIO22
# Reader 3: Pin7 - GPIO4
# Reader 4: Pin37 - GPIO26
# Reader 5: Pin13 - GPIO27
# Reader 6: Pin36 - GPIO16
reader1_pin = DigitalInOut(board.D24)
reader2_pin = DigitalInOut(board.D22)
reader3_pin = DigitalInOut(board.D4)
reader4_pin = DigitalInOut(board.D26)
reader5_pin = DigitalInOut(board.D27)
reader6_pin = DigitalInOut(board.D16)

readers = []
tags = []
timer = [0, 0, 0, 0, 0, 0]

figures_db = {}  # figure database is a dictionary with tag id and tag name stored, based on predefined figure_db.txt. figure_db.txt is created when configuring HOORCH for the first time
gamer_figures = []  # ritter, koenigin,...
animal_figures = []  # Loewe2, Elefant1, ...

endofmessage = "#"  # chr(35)

read_continuously = True


def init():
    print("initialize the rfid readers and figure_db.txt")
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

    readers.append(PN532_SPI(spi, reader1_pin, debug=False))
    readers.append(PN532_SPI(spi, reader2_pin, debug=False))
    readers.append(PN532_SPI(spi, reader3_pin, debug=False))
    readers.append(PN532_SPI(spi, reader4_pin, debug=False))
    readers.append(PN532_SPI(spi, reader5_pin, debug=False))
    readers.append(PN532_SPI(spi, reader6_pin, debug=False))

    for n, reader in enumerate(readers):
        # ic, ver, rev, support = reader.firmware_version
        # print('Found Reader '+str(n)+' with firmware version: {0}.{1}'.format(ver, rev, support))
        reader.SAM_configuration()
        print('Initialized and configured RFID/NFC reader '+str(n+1))
        tags.append(None)

    # init figure db
    path = "./figure_db.txt"

    if os.path.exists(path):
        file = open(path, mode="r", encoding="utf-8")
        figures_id_name = file.readlines()
        file.close()

        section = 0

        for uid_name in figures_id_name:
            # empty line means section change
            if uid_name.startswith(";"):
                section += 1
            else:
                (key, val) = uid_name.split(";")
                figures_db[key] = val[:val.find("\n")]

                if section == 2:
                    gamer_figures.append(
                        uid_name[uid_name.find(";")+1:uid_name.find("\n")])
                elif section == 3:
                    animal_figures.append(
                        uid_name[uid_name.find(";")+1:uid_name.find("\n")-1])

    continuous_read()


def continuous_read():

    for index, r in enumerate(readers):

        mifare = False

        tag_uid = r.read_passive_target(timeout=0.2)
        # safe energy - breaks reading of some readers?
        r.power_down()

        if tag_uid:
            # convert byte_array tag_uid to string id_readable: 4-7-26-160
            id_readable = ""
            for counter, number in enumerate(tag_uid):
                if counter < 4:
                    id_readable += str(number)+"-"
                else:
                    id_readable = id_readable[:-1]
                    break

            # reader has issues with reading mifare cards, stick with the tag_uid
            if id_readable.endswith("-"):
                # print("mifare chip!")#
                id_readable = id_readable[:-1]
                mifare = True

            # check if tag id in figure db
            try:
                tag_name = figures_db[id_readable]

            # id_readable is not in figures_db
            except:

                # reader has issues with reading content of mifare cards, stick with the tag_uid
                if mifare:
                    tag_name = id_readable
                else:

                    # read tag content to get the tag name
                    read_message = ""

                    breaker = False

                    try:
                        for i in range(7, 14):
                            block = r.ntag2xx_read_block(i)
                            # print(block)
                            for character in block:
                                if character != ord(endofmessage):
                                    read_message += chr(character)
                                else:
                                    breaker = True
                                    break

                            if breaker:
                                break

                    # if tag was removed before it was properly read
                    except TypeError:
                        print(
                            "Error while reading RFID-tag content. Tag was probably removed before reading was completed.")
                        # Die Figur konnte nicht erkannt werden. Lass sie länger auf dem Feld stehen.
                        audio.play_full("TTS", 199)
                        break

                    # remove unicode control characters from read string
                    read_message = "".join(
                        ch for ch in read_message if unicodedata.category(ch)[0] != "C")

                    # enSchaf6; - remove "en" at beginning
                    tag_name = read_message[2:]

                    # if a figure (i.e. Affe,1 or koenigin) from another game (i.e. as a replacement of a lost one) that is already defined in this game is used
                    # add another key value pair to the figures_db database
                    if tag_name in figures_db:
                        figures_db[id_readable] = tag_name

                    else:
                        # else set the unknown figure as a gamer figure, with the id_readable as tag_name
                        tag_name = id_readable

                        if tag_name not in gamer_figures:
                            gamer_figures.append(tag_name)
                            print(
                                "added new unknown gamer figure to the temporary gamer_figure list")
                        else:
                            print("unknown gamer figure detected, is already in temporary gamer_figure list")

        else:
            tag_name = None

        # keep tags in array for 1 seconds to even out reading errors
        if tag_name is None and timer[index] < time.time():
            tags[index] = tag_name  # None
            timer[index] = 0  # reset timer to 0

        if tag_name is not None:
            timer[index] = time.time()+1
            tags[index] = tag_name

    print(tags)
    
    if read_continuously:
        # rfidreaders_timer = threading.Timer(0.01,continuous_read).start()
        threading.Timer(1.0, continuous_read).start()
