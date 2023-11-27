"""
This helper outputs the UID of a found RFID tag on reader 1
"""
import time
import os
import unicodedata

import audio
import board
import busio

from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi.try_lock()
spi.configure(baudrate=12000000)
spi.unlock()

reader1_pin = DigitalInOut(board.D24)
pn532 = PN532_SPI(spi, reader1_pin, debug=False)
ic, ver, rev, support = pn532.firmware_version
pn532.SAM_configuration()

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to read ID!")

while True:

    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print(".", end="")
        # Try again if no card is available.
        if uid is not None:
            break

    # convert byte_array tag_uid to string id_readable (i.e. 4-7-26-160)
    id_readable = ""
    for counter, number in enumerate(uid):
        if counter < 4:
            id_readable += str(number)+"-"
        else:
            id_readable = id_readable[:-1]
            break

    print("")

    print("Found card with byte UID:", [hex(i) for i in uid] ," readable: ", id_readable)

    time.sleep(0.3)