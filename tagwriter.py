#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import sys
import time
import unicodedata
import board
import busio
from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from digitalio import DigitalInOut
import ndef
import leds
import audio

# gpio24
reader1_pin = DigitalInOut(board.D24)

reader = []

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

reader.append(PN532_SPI(spi, reader1_pin, debug=False))
# ic, ver, rev, support = reader[0].firmware_version
reader[0].SAM_configuration()

path = "./figure_ids.txt"
file = open(path, mode="r", encoding="utf-8")
figures = file.readlines()
file.close()

figure_database = []

#to write to block 1 and 2
#14:01:03:E1:03:E1:03:E1:03:E1:03:E1:03:E1:03:E1
#03:E1:03:E1:03:E1:03:E1:03:E1:03:E1:03:E1:03:E1
mifare_block1_2 = b'\x14\x01\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1\x03\xE1'

mifare_prefix = b'\x00\x00\x03'
ntag2_prefix = b'\x03'
#length_ndef_msg = b''
#record_header = b'\xD1'
#length_rec_type_field = b'\x01'
#payload_length = b'\'
#record_type = b'\x54'
#encoding = b'\x02' #utf8 and length of language code
#language = b'\x65\x6E'
suffix = b'\xFE'

#testdata = b'\x00\x00\x03\x10\xd1\x0e\x54\x02enHallo\xfe'

#https://community.element14.com/challenges-projects/project14/nfc-rfid/b/blog/posts/nfc-badge---update-your-badge-with-your-smartphone---ndef-and-app
#00 00 - nur für mifare!
#x03 = TLV Block tag field - 0x03=NDEF message
#!12! = length of the NDEF message 12 = 18 Bytes )
#--ndef record starts here
#xD1 = record header 0xD1= Well-Known Record
#01 = length of record type field
#0E = payload length (OE = 14 Bytes)
#54 = Record Type 0x54=Text Record
#--- here starts the payload ---
#02 = encoding (UTF8) and length of language code (2 bytes)
#65+6E = language code (en) - others: 64+65 (de)
#66:72:61:6E:7A = text string
#--- end payload ---
#--ndef record ends here
#FE - Terminator Last TLV block / suffix

key = b'\xFF\xFF\xFF\xFF\xFF\xFF'

#switch on the amp
audio.amp_sd.value = True

#write single word to ntag2 (sticker) or mifare (cards, chips)
#max length of word is 20!
def write_single(word):
    
    leds.switch_on_with_color(0)
    
    print("Place tag on reader1. Will write this to tag: "+str(word))
    #audio.espeaker("Schreibe "+str(word) +
    #               " auf den Täg. Bitte Täg auf Spielfeld 1 platzieren")
    time.sleep(2)
    tag_uid = reader[0].read_passive_target(timeout=0.2)

    if tag_uid:
        # bytearray(b'\x04q\x1b\xea\xa0e\x80')
        #print(tag_uid)

        id_readable = ""

        for counter, number in enumerate(tag_uid):
            if counter < 4:
                id_readable += str(number)+"-"
            else:
                id_readable = id_readable[:-1]
                break

        success = write_on_tag(tag_uid, word, id_readable)
        
        if success:
            print("successfully wrote "+str(word)+" to tag")
            print("now writing to database")
            audio.espeaker("Schreiben erfolgreich, Füge Täg zu Datenbank hinzu")

            db_file = open('figure_db.txt', 'a')
            # 12-56-128-34;ritter
            db_file.write(id_readable+";"+word+"\n")
            db_file.close()
        else:
            print("error occured while writing, try again.")

    else:
        print("no tag on rfid reader")
        audio.espeaker(
            "Du hast keinen Täg auf das Spielfeld platziert. Täg wurde nicht beschrieben.")


def write_set():
    audio.espeaker(
        "Wir beschreiben das gesamte Spieleset. Stelle die Figuren bei Aufruf auf Spielfeld 1")
    leds.reset()  # reset leds
    leds.switch_on_with_color(0)

    for figure in figures:
        # remove /n at the end - file figure_ids.txt needs an empty line at the end
        figure = figure[:figure.find("\n")]

        if figure == "+":
            audio.espeaker("Nächster Abschnitt")
            figure_database.append(["", ""])
            continue

        else:
            success = False
            audio.espeaker("Nächster Figur:")
            audio.espeaker(figure)
            
            while not success:

                tag_uid = None
                
                audio.espeaker("Figur stehen lassen")

                while not tag_uid:
                    tag_uid = reader[0].read_passive_target(timeout=1.0)

                id_readable = ""

                for counter, number in enumerate(tag_uid):
                    if counter < 4:
                        id_readable += str(number)+"-"
                    else:
                        id_readable = id_readable[:-1]
                        break

                success = write_on_tag(tag_uid, figure, id_readable)

            figure_database.append([id_readable, figure])
            print("added figure to figure db")

    leds.reset()
    audio.espeaker("Ende der Datei erreicht, schreibe die Datenbank")

    db_file = open('figure_db.txt', 'w')
    for pair in figure_database:
        # 12-56-128-34;ritter
        db_file.write(str(pair[0])+";"+str(pair[1])+"\n")

    db_file.close()

def write_on_tag(tag_uid, word, id_readable):

    #en defines language, english
    record = ndef.TextRecord(word,"en")
    payload = b''.join(ndef.message_encoder([record]))
    length_ndef_msg = bytearray([len(payload)])

    if id_readable.endswith("-"):
        full_payload = mifare_prefix+length_ndef_msg+payload+suffix
    else:
        full_payload = ntag2_prefix+length_ndef_msg+payload+suffix

    data = bytearray(32)
    data[0:len(full_payload)] = full_payload
    #print(data)
    chunks = len(data)

    verify_data = bytearray(0)

    try:
        #mifare tags

        #mifare 1K layout (chip + card)
        # 1 kByte
        # 16 sectors with each 4 blocks, 16 Bytes/16 ascii characters per block

        #writeable blocks (https://support.ccs.com.ph/portal/en/kb/articles/mifare-classic-1k-memory-structure)
        # 4, 5, 6
        # 8, 9, 0A,
        # 0C, 0D, 0E,...
        if id_readable.endswith("-"):
            id_readable = id_readable[:-1]
            
            #64 byte bytearray
            data_mifare = mifare_block1_2+data

            chunk_size = 16
            send = [data_mifare[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
            #print(send)

            #write 16 bytes to block 1 and 2 and blocks 4 and 5
            for i, s in enumerate(send):
                x = i+1
                if x>2:
                    x = x+1

                print("Authenticating block "+str(x))
                #print("Authenticating block "+str(4+i))
                authenticated = reader[0].mifare_classic_authenticate_block(tag_uid, x, MIFARE_CMD_AUTH_B, key)
                if not authenticated:
                    print("Authentication failed!")
                
                reader[0].mifare_classic_write_block(x, s)

                # Read blocks 4+5 only!
                if x>3:
                    verify_data.extend(reader[0].mifare_classic_read_block(x))

        #ntag2 tags
        else:
            chunk_size = 4
            send = [data[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
            
            #write 4 bytes to blocks 4 to 11
            #8 blocks x 4 byte = 32 bytes/ascii characters
            for i, s in enumerate(send):
                #print("write "+str(s)+" to block"+str(4+i))
                j = reader[0].ntag2xx_write_block(4+i, s)

            time.sleep(0.5)

            # Read blocks
            for i in range(4, 12):
                verify_data.extend(reader[0].ntag2xx_read_block(i))
    # if tag was removed before it was properly read
    except TypeError:
        print(
            "Error while reading RFID-tag content. Tag was probably removed before reading was completed.")
        # Die Figur konnte nicht erkannt werden. Lass sie länger auf dem Feld stehen.
        audio.play_full("TTS", 199)

    #print(verify_data)
    
    return verify_data == data



if __name__ == "__main__":
    if len(sys.argv) > 1:
        write_single(sys.argv[1])
    else:
        write_set()
