#!/usr/bin/env python3
# -*- coding: UTF8 -*-
import rfidreaders
import audio
import re
import time
import os
import subprocess


def start():
	output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	
	#if wifi is running
	if output is not None:
		audio.espeaker("Wifi ist schon gestartet. Die IP-Adresse lautet")
		os.system("hostname -I | cut -f1 -d' ' | espeak -v de+f2 -g 10 --stdout | aplay -D 'default'")
	
	else:
		audio.espeaker("Wifi wird gestartet. Dies kann einen Augenblick dauern.")
		#os.system("rfkill unblock wifi")
		time.sleep(10)
		audio.espeaker("Die IP-Adresse lautet")
		os.system("hostname -I | cut -f1 -d' ' | espeak -v de+f2 -g 10 --stdout | aplay -D 'default'")
		
	print("start wifi")
	

def stop():
	print("stop wifi")
	
	output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	
	#if wifi is already stopped
	if output is None:
		audio.espeaker("Wifi ist schon gestoppt")
	else:
		#os.system("rfkill block wifi")
		audio.espeaker("Wifi wurde gestoppt")