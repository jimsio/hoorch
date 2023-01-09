#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import audio
import time
import datetime
import rfidreaders
import leds
import os
import random
import copy
import subprocess

defined_figures = rfidreaders.gamer_figures

def start():

	audio.play_full("TTS",60) #Wir spielen die Geschichte für deine Figur ab

	leds.reset() #reset leds

	audio.play_full("TTS",5) #Stelle deine Figur auf eines der Spielfelder

	audio.play_file("sounds","waiting.mp3") # play wait sound
	leds.rotate_one_round(1.11)

	if "ENDE" in rfidreaders.tags:
		return

	players = copy.deepcopy(rfidreaders.tags)
	#check if player tag is predefined in definded_tags xor starts with number (then it's an unknown tag)
	for i,p in enumerate(players):
		if p not in defined_figures:
			players[i] = None

	figure_count = sum(x is not None for x in players)
	if figure_count is 0:
		audio.play_full("TTS",59) # Du hast keine Spielfigur auf das Spielfeld gestellt
		return

	#time.sleep(1)
	if "ENDE" in rfidreaders.tags:
		return

	recordings_list = os.listdir("./data/figures/")
	figure_dir = "./data/figures/"+figure_id

	#remove figures without a recorded story from list
	for i, figure_id in enumerate(players):
		if figure_id in recordings_list and figure_id+'.mp3' in os.listdir(figure_dir):
			continue
		else:
			players[i] = None

	figure_count = sum(x is not None for x in players)
	if figure_count is 0:
		audio.play_full("TTS",59) # ToDo: Keine deiner Spielfiguren hat eine Geschichte gespeichert.
		return

	#switch on leds at player field
	leds.switch_on_with_color(players, (100,100,100))

	audio.play_full("TTS",5+figure_count) #ToDo: x figuren haben eine geschichte gespeichert

	if "ENDE" in rfidreaders.tags:
		return

	start = True
	for i, figure_id in enumerate(players):
		leds.reset()
		if figure_id is not None:
			#leds.led_value[i] = 100
			leds.switch_on_with_color(i, (0,255,0))

			if start: #at start
				if figure_count > 1:
					audio.play_full("TTS",12+i) #Es beginnt die Spielfigur auf Spielfeld x
				start = False
				audio.play_full("TTS",61) # Ich Spiele dir jetzt deine Geschichte vor, wenn du stoppen willst nimm deine Spielfigur vom Spielfeld
			else:
				audio.play_full("TTS",47+i) # Die nächste Spielfigur steht auf Spielfeld x

			if "ENDE" in rfidreaders.tags:
				return

			#when figure folder exists and contains i.e. roboter.mp3
			if figure_id in recordings_list and figure_id+'.mp3' in os.listdir(figure_dir):
				#play story
				audio.play_story(figure_id)
				waitingtime = time.time() + float(subprocess.run(['soxi','-D',figure_dir+'/'+figure_id+'.mp3'], stdout=subprocess.PIPE).stdout.decode('utf-8'))
				print(waitingtime)
			else:
				audio.play_full("TTS",62) #Du hast noch keine Geschichte aufgenommen!
				continue

			while True:
				if rfidreaders.tags[i] != figure_id or waitingtime < time.time() or "ENDE" in rfidreaders.tags:
					audio.kill_sounds()
					break

			if "ENDE" in rfidreaders.tags:
				return
