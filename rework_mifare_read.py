"""
This example shows connecting to the PN532 and writing & reading a mifare classic
type RFID tag
"""
import time
import os
import unicodedata

import audio
import board
import busio

from adafruit_pn532.spi import PN532_SPI
import digitalio
from digitalio import DigitalInOut
import RPi.GPIO as GPIO

from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi.try_lock()
spi.configure(baudrate=12000000)
spi.unlock()

reader1_pin = DigitalInOut(board.D24)
pn532_reader = PN532_SPI(spi, reader1_pin, debug=False)
ic, ver, rev, support = pn532_reader.firmware_version
pn532_reader.SAM_configuration()

print("Found PN532 mifare with firmware version: {0}.{1}".format(ver, rev))

print("Waiting for RFID/NFC card to read!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

tag_uid = None
last_block = 8
endofmessage = "#"

while True:
    # Check if a card is available to read
    tag_uid = pn532_reader.read_passive_target(timeout=1.0)
    print(".", end="")

    if tag_uid is not None:
        id_readable = ""
        for counter, number in enumerate(tag_uid):
            id_readable += str(number)+"-"
        id_readable = id_readable[:-1]
        print("tag_uid readable: " + str(id_readable))
        time.sleep(1)
        break

while True:
    # read from tag - has issues, reading error occurs quite often...
    read_message = ""

    for i in range(4, last_block+1):
        while not pn532_reader.mifare_classic_authenticate_block(tag_uid, i, MIFARE_CMD_AUTH_B, key):
            print("authentication error")
            time.sleep(1)

        print("authentication successful")
        block = pn532_reader.mifare_classic_read_block(i)
        print(block)
