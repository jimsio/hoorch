# Example of detecting and reading a block from a MiFare classic NFC card.
# Author: Tony DiCola & Roberto Laricchia
# MiFare Classic modification: Francesco Crisafulli
#
# Copyright (c) 2015 Adafruit Industries

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
pn532_reader = PN532_SPI(spi, reader1_pin, debug=False)
ic, ver, rev, support = pn532_reader.firmware_version
pn532_reader.SAM_configuration()

print("Found PN532 mifare with firmware version: {0}.{1}".format(ver, rev))

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

tag_uid = None

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
		time.sleep(3)
    
"""	if tag_uid is not None:
		break

id_readable = ""
for counter, number in enumerate(tag_uid):
	id_readable += str(number)+"-"
id_readable = id_readable[:-1]
print("tag_uid readable: " + str(id_readable))

#use Data-sectors: 4-6
#20 zeichen max, keine umlaute

#HalloWerIstDennDaDie
#16 bytes immer vollmachen, bei anderem tag waren es 4 bytes

# Write 16 byte block.
lang = "en"
message = "HalloWerIstDennDaDie"
endofmessage = "#"
message = lang+message+endofmessage

chunks, chunk_size = len(message), 16
send = [message[i:i+chunk_size] for i in range(0, chunks, chunk_size)]

last_block = None

#write to tag - has issues, writing error occurs quite often...
for i, s in enumerate(send):
	print("Authenticating block " +str(4+i))
	while not pn532_reader.mifare_classic_authenticate_block(tag_uid, 4+i, MIFARE_CMD_AUTH_B, key):
	#if not auth:
		time.sleep(2)
		print("authentication error")

	while len(s) != 16:
		s += chr(0)
		
	while not pn532_reader.mifare_classic_write_block(4+i, s.encode()):
		print("writing error")
		time.sleep(2)
	
	last_block = 4+i


#read from tag - has issues, reading error occurs quite often...
read_message = ""

for i in range(4,last_block+1):
	while not pn532_reader.mifare_classic_authenticate_block(tag_uid, i, MIFARE_CMD_AUTH_B, key):
		print("authentication error")
		time.sleep(2)
		
	block = pn532_reader.mifare_classic_read_block(i)

	for character in block:
		if character != ord(endofmessage):
			read_message += chr(character)
			print(read_message)
		else:
			break

read_message = "".join(ch for ch in read_message if unicodedata.category(ch)[0]!="C")
print(read_message)
"""