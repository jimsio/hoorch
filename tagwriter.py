#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import threading
import sys
import time
import copy
import unicodedata
import board
import busio
from adafruit_pn532.spi import PN532_SPI
import digitalio
from digitalio import DigitalInOut
import RPi.GPIO as GPIO
import leds
import audio

#gpio24
reader1_pin = DigitalInOut(board.D24)

reader = []

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

reader.append(PN532_SPI(spi, reader1_pin, debug=False))
#ic, ver, rev, support = reader[0].firmware_version
reader[0].SAM_configuration()

path = "./figure_ids.txt"
file = open(path, mode="r", encoding="utf-8")
figures = file.readlines()
file.close()

lang = "en"
endofmessage = "#" #chr(35)
#chr(32) = ' ' try this?
#chr(0) = '\x00' or this?

figure_database = []


def write_single(message):
	#mifare = False

	audio.espeaker("Schreibe "+str(message)+" auf den Täg. Bitte Täg auf Spielfeld 1 platzieren")
	leds.reset() #reset leds
	leds.led_value = [1,0,0,0,0,0]
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
		#remove "en" at beginning
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

	mifare = False

	for figure in figures:
		#remove /n at the end - file figure_ids.txt needs an empty line at the end
		figure = figure[:figure.find("\n")]

		if figure == "+":
			audio.espeaker("Nächster Abschnitt")
			figure_database.append(["", ""])
			continue

		else:
			valid = False

			while not valid:

				tag_uid = None
				id_readable = ""

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
					#print(send)

					for i, s in enumerate(send):
						while len(s) != 4:
							s += "#"

						k = 0

						while not reader[0].ntag2xx_write_block(7+i,s.encode()):
							print("Failed to write {0} to at block {1}.".format(s, 7+i))

							k += 1

							if k == 6:
								print("To many false writings. Terminate for this tag block. try-block will start loop for this tag again")
								break

					time.sleep(0.5)

					#read for verification
					read_message = ""

					breaker = False

					try:
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


					#if tag was removed before it was properly read
					except TypeError:
						print("Error while reading RFID-tag content. Tag was probably removed before reading was completed.")
						#audio.espeaker("Täg konnte nicht gelesen werden. Lass ihn länger auf dem Feld stehen!")
						audio.play_full("TTS",199) #Die Figur konnte nicht erkannt werden. Lass sie länger auf dem Feld stehen.


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
		write_single(sys.argv[1])
	else:
		write_set()
