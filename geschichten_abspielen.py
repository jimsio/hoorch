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

	players = copy.deepcopy(rfidreaders.tags)
	#check if player tag is predefined in definded_tags xor starts with number (than it's an unknown tag)
	for i,p in enumerate(players):
		if p not in defined_figures:
			players[i] = None
	
	figure_count = sum(x is not None for x in players) 
	if figure_count is 0:
		audio.play_full("TTS",59) # Du hast keine Spielfigure auf das Spielfeld gestellt
		audio.play_full("TTS",54) # Das Spiel ist zu Ende
		return

	time.sleep(3)
	audio.play_full("TTS",5+figure_count)

	start = True
	for i, figure_id in enumerate(players):
		leds.reset()
		if figure_id is not None:
			leds.led_value[i] = 100
			
			if start: #at start
				audio.play_full("TTS",12+i) #Es beginnt die Spielfigur auf Spielfeld x
				start = False
				audio.play_full("TTS",61) # Ich Spiele dir jetzt deine Geschichte vor, wenn du stoppen willst nimm deine Spielfigur vom Spielfeld 
			else:
				audio.play_full("TTS",47+i) # Die nächste Spielfigur steht auf Spielfeld x
			
			try:
				files = os.listdir("./data/figures/"+figure_id)
				print(files)
			except:
				audio.play_full("TTS",62) #Du hast noch keine Geschichte aufgenommen!
				break
			
			print(files)
			#play story
			audio.play_story(figure_id)
			waitingtime = time.time() + float(subprocess.run(['soxi','-D','./data/figures/'+figure_id+'/'+files[0]], stdout=subprocess.PIPE).stdout.decode('utf-8'))

			while True:
				if rfidreaders.tags[i] != figure_id or waitingtime < time.time():
					audio.kill_sounds()
					break
					
	#audio.play_full("TTS",54) #Das Spiel ist zu Ende
	

