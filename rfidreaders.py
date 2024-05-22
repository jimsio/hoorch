#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import time
import threading
import os
#import unicodedata
import board
import busio
from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
#import digitalio
from digitalio import DigitalInOut
import ndef
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

figures_db = {}  # figure database is a dictionary with tag id and tag name stored, based on predefined figure_db.txt. figure_db.txt is created when configuring HOORCH for the first time (and is based on tag names in figure_ids.txt)
gamer_figures = []  # ritter, koenigin,...
animal_figures = []  # Loewe2, Elefant1, ...

endofmessage = "#"  # chr(35)

read_continuously = True
currently_reading = False

auth_key = b'\xFF\xFF\xFF\xFF\xFF\xFF'


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
        time.sleep(0.03)

    # init figure db
    path = "./figure_db.txt"

    if os.path.exists(path):
        with open(path, mode="r", encoding="utf-8") as file:
            figures_id_name = file.readlines()
        
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
    
    global currently_reading

    for index, r in enumerate(readers):

        mifare = False

        currently_reading = True

        tag_uid = r.read_passive_target(timeout=0.2)
        
        if tag_uid:
            # convert byte_array tag_uid to string id_readable (i.e. 4-7-26-160)
            id_readable = ""
            for counter, number in enumerate(tag_uid):
                if counter < 4:
                    id_readable += str(number)+"-"
                else:
                    id_readable = id_readable[:-1]
                    break

            # mifare id has minus at the end, remove it here
            if id_readable.endswith("-"):
                id_readable = id_readable[:-1]
                mifare = True

            # check if tag id in figure db
            try:
                tag_name = figures_db[id_readable]

            # id_readable is not in figures_db
            except KeyError:
                
                if mifare:
                    tag_name = read_from_mifare(r, tag_uid)
                else:
                    tag_name = read_from_ntag2(r)

                # power down to safe energy, breaks readers?
                r.power_down()
                
                if tag_name == "#error#":
                    continue

                currently_reading = False

                #if tag_name is empty, use id_readable
                if not tag_name:
                    #print("tag is empty, use id_readable")
                    tag_name = id_readable

                # if a figure (i.e. Loewe0 or koenigin) from another game (i.e. as a replacement of a lost one) that is already defined in this game is used
                # add another key value pair to the figures_db database
                elif tag_name in figures_db:
                    figures_db[id_readable] = tag_name       

                else:
                    # else set the unknown figure as a gamer figure with read tag_name
            
                    if tag_name not in gamer_figures:
                        gamer_figures.append(tag_name)
                        print(
                            "added new unknown gamer figure to the temporary gamer_figure list")
                    else:
                        pass
                        #print("unknown gamer figure already in temporary gamer_figure list")

        else:
            tag_name = None

        # keep tags in array for 1 seconds to even out reading errors
        if tag_name is None and timer[index] < time.time():
            tags[index] = tag_name  # None
            timer[index] = 0  # reset timer to 0

        if tag_name is not None:
            timer[index] = time.time()+1
            tags[index] = tag_name
        
        #sleep for 0.2 seconds between readers to avoid heavy power load
        time.sleep(0.2)

    print(tags)

    if read_continuously:
        #only read when not playing or recording audio - shouldnt be done, need it for ending recording
        #while ('play' or 'rec') in subprocess.run(['ps', 'ax'], stdout=subprocess.PIPE).stdout.decode('utf-8'):
            #time.sleep(0.2)

        threading.Timer(0.02, continuous_read).start()
        
def read_from_mifare(reader, tag_uid):
    read_data = bytearray(0)
    
    try:
        #read 16 bytes from blocks 4 and 5
        for i in range(4, 6):
            #print("Authenticating block "+str(i))
                authenticated = reader.mifare_classic_authenticate_block(tag_uid, i, MIFARE_CMD_AUTH_B, auth_key)
                if not authenticated:
                    print("Authentication failed!")
                # Read blocks
                read_data.extend(reader.mifare_classic_read_block(i))
        
        to_decode = read_data[4:read_data.find(b'\xfe')]
        return list(ndef.message_decoder(to_decode))[0].text
    
    except TypeError:
        print("Error while reading RFID-tag content. Tag was probably removed before reading was completed.")
        # Die Figur konnte nicht erkannt werden. Lass sie länger auf dem Feld stehen.
        audio.play_full("TTS", 199)

        return "#error#"
    
    except ndef.record.DecodeError as e:
        print("ndeflib Error while decoding")
        print(e)

        return "error#"

def read_from_ntag2(reader):
    read_data = bytearray(0)
    
    #read 4 bytes from blocks 4-11
    try:
        for i in range(4, 12):
            read_data.extend(reader.ntag2xx_read_block(i))
        to_decode = read_data[2:read_data.find(b'\xfe')]
    
        return list(ndef.message_decoder(to_decode))[0].text

    # if tag was removed before it was properly read
    except TypeError:
        print("Error while reading RFID-tag content. Tag was probably removed before reading was completed.")
        # Die Figur konnte nicht erkannt werden. Lass sie länger auf dem Feld stehen.
        audio.play_full("TTS", 199)
        
        return "#error#"
    
    except ndef.record.DecodeError as e:
        print("ndeflib Error while decoding")
        print(e)
        
        return "error#"


#except KeyboardInterrupt:
#   for r in readers:
#    r.power_down()