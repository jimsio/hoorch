#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import board
import threading
import sys
import time
import busio
from adafruit_pn532.spi import PN532_SPI
import digitalio
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
import audio
import copy
import unicodedata
import leds


#gpio24
reader1_pin = DigitalInOut(board.D24)


reader = []

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi.try_lock()
spi.configure(baudrate=12000000)
spi.unlock()

reader.append(PN532_SPI(spi, reader1_pin, debug=False))
ic, ver, rev, support = reader[0].firmware_version
reader[0].SAM_configuration()

#TODO
#https://circuitpython.readthedocs.io/projects/pn532/en/latest/api.html
''' for mifare (maybe card)
authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")

# Set 16 bytes of block to 0xFEEDBEEF
data = bytearray(16)
data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# Write 16 byte block.
pn532.mifare_classic_write_block(4, data)
# Read block #6
print(
    "Wrote to block 4, now trying to read that data:",
    [hex(x) for x in pn532.mifare_classic_read_block(4)],
)
'''

path = "./figure_ids.txt"
file = open(path, mode="r", encoding="utf-8")
figures = file.readlines()
file.close()

lang = "en"
endofmessage = "#" #chr(35)
#chr(32) = ' ' try this?
#chr(0) = '\x00' or this?

figure_database = []


def write_single():
	
	message = sys.argv[1]
	
	audio.espeaker("Schreibe "+str(message)+" auf den Täg. Bitte Täg auf Spielfeld 1 platzieren")
	time.sleep(2)
	tag_uid = reader[0].read_passive_target(timeout=0.05)
	
	if tag_uid:
		#bytearray(b'\x04q\x1b\xea\xa0e\x80')
		print(tag_uid)
		
		id_readable = ""
		
		for counter, number in enumerate(tag_uid):
			if counter < 4:
				id_readable += str(number)+"-"
			else:
				id_readable = id_readable[:-1]
				break
	
		print("write "+str(message)+ " on tag with tag_uid: " +id_readable)
		
		#write
		message = lang+message+endofmessage
		
		chunks, chunk_size = len(message), 4
		send = [message[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
		
		for i, s in enumerate(send):
			while len(s) != 4:
				s += chr(0)
			j = reader[0].ntag2xx_write_block(7+i,s.encode())
			#print(j)

		time.sleep(1)
		
		#read for verification
		read_message = ""
		
		breaker = False
		
		for i in range(7,14):
			block = reader[0].ntag2xx_read_block(i)
			print(block) #bytearray(b'en9\t')
			for character in block:
				if character != ord(endofmessage):
					read_message += chr(character)
				else:
					breaker = True
					break
			
			if breaker:
				break
		
		#remove unicode control characters (\t) from read string
		read_message = "".join(ch for ch in read_message if unicodedata.category(ch)[0]!="C")
		#remove "en" at beginning ?
		read_message = read_message[2:]
		
		print("wrote "+read_message+" to tag")
		audio.espeaker("Schreiben erfolgreich, Füge Täg zu Datenbank hinzu")
		
		db_file = open('figure_db.txt','a')
		#12-56-128-34;ritter
		db_file.write(id_readable+";"+read_message+"\n")
		db_file.close()
		
	
	else:
		print("no tag on rfid reader")
		audio.espeaker("Du hast keinen Täg auf das Spielfeld platziert. Täg wurde nicht beschrieben.")

def write_set():
	audio.espeaker("Wir beschreiben das gesamte Spieleset. Stelle die Figuren bei Aufruf auf Spielfeld 1")
	leds.reset() #reset leds
	leds.led_value = [1,0,0,0,0,0]
	
	for figure in figures:
		#remove /n at the end - file figure_ids.txt needs an empty line at the end
		figure = figure[:figure.find("\n")]
		
		if figure == "+":
			audio.espeaker("Nächster Abschnitt")
			figure_database.append(["", ""])
			continue
		
		else:
			valid = False
			tag_uid = None
			id_readable = ""
			
			while not valid:
			
				audio.espeaker("Nächster Figur:")
				audio.espeaker(figure)
				audio.espeaker("Figur stehen lassen")
				
				while not tag_uid:
					tag_uid = reader[0].read_passive_target(timeout=1.0)
				
				for counter, number in enumerate(tag_uid):
					if counter < 4:
						id_readable += str(number)+"-"
					else:
						id_readable = id_readable[:-1]
						break
						
				#reader has issues with reading mifare cards, stick with the tag_uid
				if id_readable.endswith("-"):
					print("mifare chip!")
					id_readable = id_readable[:-1]
					mifare = True
			
				print(id_readable)
				
				if not mifare:
					#write
					message = lang+figure+endofmessage
					print("message: " +str(message))
					chunks, chunk_size = len(message), 4
					send = [message[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
					print(send)
					
					for i, s in enumerate(send):
						while len(s) != 4:
							s += "#"
						j = reader[0].ntag2xx_write_block(7+i,s.encode())
						#print("j: " + str(j))
						
					time.sleep(1)
				
					#read for verification
					read_message = ""
					
					breaker = False
					
					for i in range(7,14):
						block = reader[0].ntag2xx_read_block(i)
						print(block)
						for character in block:
							if character != ord(endofmessage):
								read_message += chr(character)
							else:
								breaker = True
								break
						
						if breaker:
							break
					
					#remove unicode control characters from read string
					read_message = "".join(ch for ch in read_message if unicodedata.category(ch)[0]!="C")
					
					# enFRAGEZEICHEN#
					message = message[2:-1]
					#read_message has no #/endofmessage at end, this was checked during reading
					read_message = read_message[2:]
					
					valid = message == read_message
					print("valid " + str(valid))
				
				else:
					valid = True
			
			figure_database.append([id_readable, figure])
			print("added figure to figure db")

	leds.reset()
	audio.espeaker("Ende der Datei erreicht, schreibe die Datenbank")
	
	db_file = open('figure_db.txt','w')
	for pair in figure_database:
		#12-56-128-34;ritter
		db_file.write(str(pair[0])+";"+str(pair[1])+"\n")

	db_file.close()
	

if __name__ == "__main__":
	if len(sys.argv) > 1:
		write_single()
	else:
		write_set()