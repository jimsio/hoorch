#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import audio
import time
import rfidreaders
import leds
import os
import random
import copy

defined_figures = rfidreaders.gamer_figures
defined_animals = rfidreaders.animal_figures

def start():
	audio.play_full("TTS",4) #Ihr spielt das Spiel Tierlaute erraten.
	leds.reset() #reset leds
	
	audio.play_full("TTS",5) #Stelle deine Figur auf eines der Spielfelder
	
	audio.play_file("sounds","waiting.mp3") # play wait sound
	leds.rotate_one_round(1.11)
	
	if "ENDE" in rfidreaders.tags:
		return

	#check for figures on board, filter other tags
	players = copy.deepcopy(rfidreaders.tags)
	
	for i,p in enumerate(players):
		if p not in defined_figures:
			players[i] = None
	
	figure_count = sum(x is not None for x in players) 

	time.sleep(1)
	if figure_count is 0:
		audio.play_full("TTS",59) #Du hast keine Spielfigure auf das Spielfeld gestellt.
		return
	
	audio.play_full("TTS",5+figure_count) # Es spielen x Figuren mit

	rounds = 5 # 1-5 rounds possible
	audio.play_full("TTS",20+rounds) #Wir spielen 1-5 Runden
	points = [0,0,0,0,0,0]
	
	isthefirst = True
	for r in range(0,rounds):
		#print(players)
		for i,p in enumerate(players):
			if p is not None:
				leds.reset()
				leds.led_value[i] = 100
				
				if "ENDE" in rfidreaders.tags:
					return
				
				if r == 0 and isthefirst == True: #first round
					isthefirst = False
					audio.play_full("TTS",12+i) #Es beginnt die Spielfigur auf Spielfeld x
					audio.play_full("TTS",19) #Ich spiele dir jetzt die Laute eines Tiers vor. Wenn du das Tier erkennst, tausche deine Spielfigur gegen den Tier-Spielstein.
				elif figure_count == 1:
					audio.play_full("TTS",67) # Du bist nochmal dran
				else:
					audio.play_full("TTS",48+i) # Die nächste Spielfigur steht auf Spielfeld x

				animal = random.choice(defined_animals)
				audio.play_file("animal_sounds",animal)
				animal = animal.replace(".mp3","")

				while True:
					if "ENDE" in rfidreaders.tags:
						audio.kill_sounds()
						return
						
					if not audio.file_is_playing(animal+".mp3"):
						audio.play_file("animal_sounds",animal+".mp3")

					figure_on_field = copy.deepcopy(rfidreaders.tags[i])
					#remove single digit from the end (Hahn1)
					if figure_on_field is not None:
						figure_on_field = figure_on_field[:-1]
					
					if figure_on_field != None and figure_on_field != p and figure_on_field in defined_animals:
						audio.kill_sounds()

						if figure_on_field == animal:
							time.sleep(0.2)
							audio.play_full("TTS",27)
							print("richtig")
							audio.play_file("sounds","winner.mp3")
							time.sleep(0.2)
							points[i] += 1
							print("Du hast schon "+str(points[i])+" richtige Antworten")
							rfidreaders.tags[i] = None
							break
						else:
							time.sleep(0.2)
							audio.play_full("TTS",26)
							print("falsch")
							audio.play_file("sounds","loser.mp3")
							time.sleep(0.2)
							rfidreaders.tags[i] = None
							break
	
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
	
	leds.reset()
