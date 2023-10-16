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
pn532 = PN532_SPI(spi, reader1_pin, debug=False)
ic, ver, rev, support = pn532.firmware_version
pn532.SAM_configuration()


ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
    # Try again if no card is available.
    if uid is not None:
        break

print("")

print("Found card with UID:", [hex(i) for i in uid])

#mifare 1K layout (chip + card)
# 1 kByte

# 16 Sektoren zu je 4 Blöcken (16 Bytes/16 Ascii Characters pro Block)

#writeable blocks (https://support.ccs.com.ph/portal/en/kb/articles/mifare-classic-1k-memory-structure)
# 4, 5, 6
# 8, 9, 0A,
# 0C, 0D, 0E,...

#allow only 16 ascii characters, so i only need one block, block 4
# 2 characters for prefix "en", 1 for suffix "#", so my word can have 13 characters!

print("Authenticating block 4 ...")
authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")


data = bytearray(16)

lang = "en"
message = "MANFREd" #can be 13 characters long
endofmessage = "#"
message = lang+message+endofmessage

data[0:len(message)] = message.encode()

print(data)

# Set 16 bytes of block to 0xFEEDBEEF
#data = bytearray(16)
#data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# Write 16 byte to block 4.
pn532.mifare_classic_write_block(4, data)

# Read block
print(
    "Wrote to block 4, now trying to read that data:",
    [hex(x) for x in pn532.mifare_classic_read_block(4)],
)