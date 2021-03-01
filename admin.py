#!/usr/bin/env python3
# -*- coding: UTF8 -*-
import rfidreaders
import audio
import time
import os
import subprocess
import datetime

def main():
	# 2 minutes until exit if no user interaction occurs
	audio.espeaker("Sie befinden sich im Admin-Menü.")
	audio.espeaker("Verwenden Sie die Zahlenkarten um Einstellungen vorzunehmen.")
	audio.espeaker("1 - WeiFei-Konfiguration.")
	audio.espeaker("2 - Software aktualisieren.")
	audio.espeaker("3 - Spielfiguren-Set löschen.")
	#audio.espeaker("4 - Start server - brauchen wir das?")
	audio.espeaker("Ende-Täg zum Beenden.")

	admin_exit_counter = time.time() + 120

	while admin_exit_counter > time.time() or not "ENDE" in rfidreaders.tags:

		for tag_name in rfidreaders.tags:
			if tag_name != None and re.search("^[A-z]*[0-9]$", tag_name):
				op = int(tag_name[-1]) #1 from Hahn1

				if op == 1:
					wifi()
					admin_exit_counter = time.time() + 120
				elif op == 2:
					#git update
					git()
					admin_exit_counter = time.time() + 120
				elif op == 3:
					new_set()

				elif op == 4:
					#start server
					start_server()
					admin_exit_counter = time.time() + 120

def start_server():
	#needed???
	pass

def new_set():
	#delete figure_db.txt, restart hoorch
	os.rename("figure_db.txt","figure_db-{0}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
	audio.espeaker("Figuren-Datenbank gelöscht. Ich starte jetzt neu.")
	os.system("reboot")

def git():
	#git update, restart hoorch
	output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	#not connected to a wifi
	if output is None:
		audio.espeaker("Weifei nicht verbunden.")
		audio.espeaker("Öffne zuerst mit der Zahlenkarte 1 die WeiFei Konfiguration.")

	else:
		audio.espeaker("Aktualisierung wird gestartet. Dies kann einige Minuten dauern. Hoorch startet anschließend neu.")
		subprocess.run(['git','pull'], stdout=subprocess.PIPE)
		os.system("reboot")

def wifi():

	rfkill_output = subprocess.run(['rfkill','list','wifi'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	#wifi blocked / off
	if "yes" in rfkill_output:
		audio.espeaker("Weifei ist ausgeschaltet.")
		audio.espeaker("Soll ich es einschalten?")

		while True:
			if "JA" in rfidreaders.tags:
				audio.espeaker("Weifei wird gestartet. Dies kann einen Augenblick dauern.")
				#os.system("rfkill unblock wifi")

				while not subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8'):
					time.sleep(2)

				output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')
				ip_adress = output.split(" ",1)
				print(ip_adress)

				audio.espeaker("Weifei eingeschaltet.")
				audio.espeaker("Die IP-Adresse lautet")
				audio.espeaker(ip_adress[0])

				break

			elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
				break
	#wifi on
	else:
		output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')

		#not connected to a wifi
		if output is None:
			audio.espeaker("Keine Verbindung zu einem WeiFei.")
			audio.espeaker("Verbinde dich am Handy mit dem Hotspot namens hooorch minus und dann drei Zahlen. Öffne dann im Brauser hooorch minus und die drei Zahlen Punkt local")
			audio.espeaker("Stelle dort dein lokales WeiFei ein")
			#https://davesteele.github.io/comitup/man/comitup-cli.pdf maybe
			#comitup.state()

		#connected to a wifi
		else:
			audio.espeaker("Wifi verbunden.")
			ip_adress = output.split(" ",1)
			print(ip_adress)

			#say adress twice
			for i in range(2):
				audio.espeaker("Die IP-Adresse lautet")
				audio.espeaker(ip_adress[0])
			time.sleep(2)

			audio.espeaker("Soll ich es ausschalten?")

			while True:
				if "JA" in rfidreaders.tags:
					#os.system("rfkill block wifi")
					audio.espeaker("Wifi wurde gestoppt")
					break

				elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
					break

	audio.espeaker("Wifi-Konfiguration beendet")
