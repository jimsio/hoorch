#!/usr/bin/env python3
# -*- coding: UTF8 -*-
import rfidreaders
import audio
import time
import os
import subprocess
import datetime
import re
import dbus


def main():

	breaker = False

	# 2 minutes until exit if no user interaction occurs
	audio.espeaker("Sie befinden sich im Admin-Menü.")
	audio.espeaker("Verwenden Sie die Zahlenkarten um Einstellungen vorzunehmen.")
	audio.espeaker("1 - WeiFei-Konfiguration.")
	audio.espeaker("2 - Software aktualisieren.")
	audio.espeaker("3 - Spielfiguren-Set löschen.")
	audio.espeaker("4 - Alle Geschichten archivieren")
	audio.espeaker("Ende-Täg zum Beenden.")

	admin_exit_counter = time.time() + 120

	while admin_exit_counter > time.time():

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
					#archive all figure stories
					archive_stories()
					admin_exit_counter = time.time() + 120
			elif tag_name == "ENDE":
				breaker = True
				break

		if breaker:
			break

	audio.espeaker("Admin-Menü beendet.")


def archive_stories():
	recordings_list = os.listdir("./data/figures/")

	for folder in recordings_list:
		if folder+".mp3" in os.listdir("./data/figures/"+folder+"/"):
			#print(folder+".mp3")
			os.rename("./data/figures/"+folder+"/"+folder+".mp3","./data/figures/"+folder+"/"+folder+"{0}.mp3".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

	audio.espeaker("Alle Geschichten wurden archiviert.")

def new_set():
	#delete figure_db.txt, restart hoorch
	os.rename("figure_db.txt","figure_db-{0}.txt".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
	audio.espeaker("Figuren-Datenbank gelöscht. Ich starte jetzt neu.")
	os.system("reboot")

def git():
	#git update, restart hoorch
	bus = dbus.SystemBus()
	#get comitup dbus object - https://davesteele.github.io/comitup/man/comitup.8.html
	nm = bus.get_object('com.github.davesteele.comitup', '/com/github/davesteele/comitup')

	tpl = nm.state()

	#state is either 'HOTSPOT', 'CONNECTING', or 'CONNECTED'
	state = str(tpl[0])

	if state == "HOTSPOT":
		audio.espeaker("Weifei nicht verbunden.")
		audio.espeaker("Öffne zuerst mit der Zahlenkarte 1 die WeiFei Konfiguration.")

	elif state == "CONNECTED":
		audio.espeaker("Aktualisierung wird gestartet. Dies kann einige Minuten dauern. Hoorch startet anschließend neu.")
		subprocess.run(['git','pull'], stdout=subprocess.PIPE)
		audio.espeaker("Aktualisierung beendet. Ich starte jetzt neu.")
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

		bus = dbus.SystemBus()
		#get comitup dbus object - https://davesteele.github.io/comitup/man/comitup.8.html
		nm = bus.get_object('com.github.davesteele.comitup', '/com/github/davesteele/comitup')

		tpl = nm.state()

		#state is either 'HOTSPOT', 'CONNECTING', or 'CONNECTED'
		state = str(tpl[0])

		#connection - ssid name for the current connection on the wifi device
		connection = tpl[1]

		#accesspoint hostname
		info = nm.get_info()
		hostname = str(info["apname"])

		if state == "HOTSPOT":
			audio.espeaker("Keine Verbindung zum Internet.")
			audio.espeaker("Verbinde dich am Handy mit dem Hotspot namens {0}. Öffne dann im Brauser {0} Punkt local".format(hostname))
			audio.espeaker("Stelle dort dein lokales WeLan und Passwort ein")

		#connected to a wifi
		elif state == "CONNECTED":
			audio.espeaker("Mit WeiFei {0} verbunden.".format(connection))
			output = subprocess.run(['hostname','-I'], stdout=subprocess.PIPE).stdout.decode('utf-8')
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
					audio.espeaker("Weifei wurde gestoppt")
					break

				elif "NEIN" in rfidreaders.tags or "ENDE" in rfidreaders.tags:
					break

		#connecting
		else:
			audio.espeaker("Internet in wenigen Augenblicken verfügbar. Bitte warten.")
			time.sleep(2)


	audio.espeaker("Weifei-Konfiguration beendet")
