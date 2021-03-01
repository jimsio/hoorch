"""
This example shows connecting to the PN532 and writing & reading a mifare classic
type RFID tag
"""

import board
import busio

from adafruit_pn532.spi import PN532_SPI
import digitalio
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
import time
import os
import unicodedata
import audio

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

print("Found card with UID:", [str(i) for i in uid])
#print("Found card with UID:", [hex(i) for i in uid])
print("Authenticating block 4 ...")

authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")

# Set 16 bytes of block to 0xFEEDBEEF
#data = bytearray(16)
#data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

#print("Data to write:", [str(i) for i in data])

data = bytearray()

lang = "en"
message = "ADMIN"
endofmessage = "#"
message = lang+message+endofmessage

chunks, chunk_size = len(message), 16
send = [message[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

print(send)

for i, s in enumerate(send):
	while len(s) != chunk_size:
		s += chr(0)
	print(s)
	print(s.encode())
	#j = reader[0].ntag2xx_write_block(4+i,s.encode())
	pn532.mifare_classic_write_block(4+i, s.encode())

#print("Data to write:", [str(i) for i in data])

# Write 16 byte to block 4.
#pn532.mifare_classic_write_block(4, data)
# Read block #4
print(
    "Wrote to block 4, now trying to read that data:",
    [hex(x) for x in pn532.mifare_classic_read_block(4)],
)
