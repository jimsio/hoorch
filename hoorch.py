#!/usr/bin/env python3
# -*- coding: UTF8 -*-

# require: see installer.sh

import threading
import time
import os
import subprocess
import RPi.GPIO as GPIO
import audio
import rfidreaders
import leds
import tierlaute
import geschichten_aufnehmen
import kakophonie
import tier_orchester
import geschichten_abspielen
import einmaleins
import animals_english
import admin
import tagwriter


def init():
	print ("initializiation of hardware")
	
	#initialize audio
	audio.init()
	
	audio.play_full("TTS",1)

	#initialize leds
	leds.init()

	#initialize figure_db if no tags defined for this hoorch set
	if not os.path.exists("./figure_db.txt"):
		leds.random_timer = False
		tagwriter.write_set()
	
	#start random blinker
	leds.random_timer = True

	#initialize readers
	rfidreaders.init()
	

#check_pause()

#def check_pause():
	#while "PAUSE" in rfidreaders.tags:
		#print("ich mache pause - spiel pausenmusik")
		#audio.espeaker("ich mache pause")
		#audio.play_full("TTS",1)
		#leds.reset()
		#leds.rotate_one_round(0.5)
		#leds.led_value[index] = 0
		#time.sleep(0.5)
		#leds.led_value[index] = 1
		#time.sleep(0.5)
		#leds.reset()
		
		#pause_timer1 = threading.Timer(0.01,check_pause).start()

	#pause_timer = threading.Timer(2.0,check_pause).start()

	
def main():
	print ("start main loop")
	shutdown_time = 300 #seconds until shutdown if no interaction happened
	shutdown_counter = time.time()+shutdown_time
		
	greet_time = time.time()
	
	
	#while True:
	while shutdown_counter > time.time():
		
		leds.random_timer = True
		
		if greet_time < time.time():
			audio.play_full("TTS",2) #Welches Spiel wollt ihr spielen?
			greet_time = time.time()+30
		
		## Erklärung
		if "FRAGEZEICHEN" in rfidreaders.tags:
			print("Hoorch Erklärung")
			leds.random_timer = False
			audio.play_full("TTS",65) #Erklärung
			shutdown_counter = time.time()+shutdown_time
		
		## Games
		if "Aufnehmen" in rfidreaders.tags:
			print("Geschichten aufnehmen")
			leds.random_timer = False
			#active_thread = threading.Thread(target = geschichten_aufnehmen.start(), arg=(1,))
			#active_thread.start()
			geschichten_aufnehmen.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time
			
		if "Abspielen" in rfidreaders.tags:
			print("Geschichte abspielen")
			leds.random_timer = False
			geschichten_abspielen.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time

		if "Tierlaute" in rfidreaders.tags:
			print("Tierlaute erkennen")
			leds.random_timer = False
			tierlaute.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time

		if "TierOrchester" in rfidreaders.tags:
			print("Tier-Orchester")
			leds.random_timer = False
			tier_orchester.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time

		if "Kakophonie" in rfidreaders.tags:
			print("Kakophonie")
			leds.random_timer = False
			kakophonie.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time
	
		if "Einmaleins" in rfidreaders.tags:
			print("Einmaleins")
			leds.random_timer = False
			einmaleins.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time

		if "Animals" in rfidreaders.tags:
			print("Animals")
			leds.random_timer = False
			animals_english.start()
			audio.play_full("TTS",54) #Das Spiel ist zu Ende
			shutdown_counter = time.time()+shutdown_time

		#NFC tools on Android: write text to tag: ADMIN#
		if "ADMIN" in rfidreaders.tags:
			admin.main()
			shutdown_counter = time.time()+shutdown_time
		
		time.sleep(0.3)
	
	#shutdown
	print("shutdown")
	audio.play_full("TTS",196) #Du hast mich lange nicht verwendet. Ich schalte mich zum Stromsparen jetzt aus.
	leds.random_timer = False
	leds.led_value = [1,1,1,1,1,1]
	#os.system("shutdown -P now")
			

if __name__ == "__main__":
	init()
	main()
