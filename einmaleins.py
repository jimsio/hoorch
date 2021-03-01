#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import audio
import time
import rfidreaders
import leds
import random
import copy
import threading
import re
import sys

defined_figures = rfidreaders.gamer_figures
#end_timer = None

'''def check_end():
	if "ENDE" in rfidreaders.tags:
		print("sys.exit")
		end_timer.cancel()
		sys.exit("End game")

	end_timer = threading.Timer(0.3,check_end).start()
'''
def start():
	#check_end()

	audio.play_full("TTS",85) #Wir üben jetzt das Einmaleins.
	leds.reset() #reset leds

	audio.play_full("TTS",86) #Es können drei Figuren mitspielen. Stellt eure Figuren auf die Felder 1, 3 oder 5, wo die Lämpchen leuchten.
	leds.led_value = [1,0,1,0,1,0]
	audio.play_file("sounds","waiting.mp3") # play wait sound
	time.sleep(6)

	#check for figures on board, filter other tags
	players = copy.deepcopy(rfidreaders.tags)

	players[1] = None
	players[3] = None
	players[5] = None

	for i,p in enumerate(players):
		if p not in defined_figures:
			players[i] = None

	figure_count = sum(x is not None for x in players)

	time.sleep(1)
	if figure_count is 0:
		audio.play_full("TTS",59) #Du hast keine Spielfigure auf das Spielfeld gestellt.
		return

	audio.play_full("TTS",5+figure_count) # Es spielen x Figuren mit

	if "ENDE" in rfidreaders.tags:
		return

	rounds = 3 # 1-5 rounds possible
	audio.play_full("TTS",20+rounds) #Wir spielen 1-5 Runden
	points = [0,0,0,0,0,0]

	if "ENDE" in rfidreaders.tags:
		return

	isthefirst = True
	for r in range(0,rounds):
		#print(players)
		for i,p in enumerate(players):
			if p is not None:
				leds.reset()
				leds.led_value[i] = 100

				if r == 0 and isthefirst == True: #first round
					isthefirst = False
					if figure_count > 1:
						audio.play_full("TTS",12+i) #Es beginnt die Spielfigur auf Spielfeld x
					audio.play_full("TTS",89) #Stelle die Zehnerstelle links neben deine Figur und die Einerstelle rechts, wo die Lämpchen leuchten.
				elif figure_count == 1:
					audio.play_full("TTS",67) # Du bist nochmal dran
				else:
					audio.play_full("TTS",48+i) # Die nächste Spielfigur steht auf Spielfeld x

				if "ENDE" in rfidreaders.tags:
					return

				num1 = random.randint(1,9)
				num2 = random.randint(1,9)
				solution = num1 * num2

				audio.play_full("TTS",87) #Wieviel ist
				audio.play_full("TTS",90+num1)
				audio.play_full("TTS",88) #mal
				audio.play_full("TTS",90+num2)
				ud = 0

				#for unit digit
				if i == 0:
					ud = 5
				else:
					ud = i-1

				#illuminate the led after and before the player field
				leds.led_value[ud] = 100
				leds.led_value[i+1] = 100

				if "ENDE" in rfidreaders.tags:
					return

				audio.play_full("TTS",190) #Du hast für die Antwort 10 Sekunden Zeit

				#blink / wait for 10 seconds
				#for b in range(1):
				if r == 0: #only play in the first round
					audio.play_file("sounds","waiting.mp3") # play wait sound 6 sec

				#leds.rotate_one_round(1.11)

				#leds blink at tens and unit fields
				for k in range(5):
					leds.led_value[i+1] = 0
					leds.led_value[ud] = 100
					time.sleep(1)
					leds.led_value[ud] = 0
					leds.led_value[i+1] = 100
					time.sleep(1)

				if "ENDE" in rfidreaders.tags:
					return

				tens = copy.deepcopy(rfidreaders.tags[i+1]) #zehnerstelle
				unit = copy.deepcopy(rfidreaders.tags[ud]) #Einerstelle

				if tens == None:
					tens = "0"

				#regex (start with capital character, zero or more characters, end with single digit) : ^[A-z]*[0-9]$
				#search with regex if unit and tens look like Hahn1
				if unit != None and re.search("^[A-z]*[0-9]$", unit) and re.search("^[A-z]*[0-9]$", tens):

					#extract the digit from string (i.e. 1 from Hahn1)
					tens_digit = int(tens[-1])*10
					#old: tens_digit = int(tens)*10

					#old: unit_digit = int(unit)
					unit_digit = int(unit[-1])

					if tens_digit+unit_digit == solution:
						audio.play_full("TTS",27) # richtig
						#audio.play_file("sounds","winner.mp3")
						time.sleep(0.5)
						points[i] += 1
						print("Du hast schon "+str(points[i])+" richtige Antworten")

					else:
						audio.play_full("TTS",26) # falsch
						#audio.play_file("sounds","loser.mp3")
						time.sleep(0.5)

				else:
					audio.play_full("TTS",191) #Du hast keine Zahlen hingestellt


				if "ENDE" in rfidreaders.tags:
					return


	# tell the points
	audio.play_full("TTS",80) #Ich verlese jetzt die Punkte
	for i, p in enumerate(players):
		if p is not None:
			leds.reset()
			leds.led_value[i] = 100
			audio.play_full("TTS",74+i) #Spielfigur auf Spielfeld 1,2...6
			time.sleep(0.2)
			print("Du hast "+str(points[i])+" Antworten richtig")
			audio.play_full("TTS",68+points[i])
			time.sleep(1)

			if "ENDE" in rfidreaders.tags:
				return

	leds.reset()
