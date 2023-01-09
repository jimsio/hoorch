#!/usr/bin/env python3
# -*- coding: UTF8 -*-

import subprocess
import time
import os

path = "./data/"

def init():
	#set environment variable for sox rec
	os.environ['AUDIODRIVER'] = "alsa"

	#set mic record level to 95% (92 in alsamixer)
	os.system("amixer -q -c 1 sset 'Mic',0 95%")

#non-blocking play
def play(folder, audiofile):
	subprocess.Popen("play "+path+"/"+folder+"/"+"{:03d}".format(audiofile)+".mp3"+"  2>/dev/null",shell=True, stdout=None, stderr=None)
	#print("playing TTS number "+str(audiofile))

def play_full(folder, audiofile):
	file_path = path+folder+"/"+"{:03d}".format(audiofile)+".mp3"
	waitingtime = float(subprocess.run(['soxi','-D',file_path], stdout=subprocess.PIPE).stdout.decode('utf-8'))
	subprocess.Popen("play "+file_path+" 2>/dev/null",shell=True, stdout=None, stderr=None)
	time.sleep(waitingtime)

#for sounds (animals, systemsounds) in /data and subsequent folders
def play_file(folder, audiofile):
	subprocess.Popen("play "+path+folder+"/"+audiofile+"  2>/dev/null",shell=True, stdout=None, stderr=None)
	print("playing file "+str(audiofile))

def play_story(figure_id):
	print("play story of " +str(figure_id))
	#increase volume by -2db for stories as their recording volume is lower
	subprocess.Popen("play -v2 "+path+"figures/"+figure_id+"/"+figure_id+".mp3"+"  2>/dev/null",shell=True, stdout=None, stderr=None)

def kill_sounds():
	subprocess.Popen("killall play",shell=True, stdout=None, stderr=None)

def file_is_playing(audiofile):
	output = subprocess.run(['ps','ax'], stdout=subprocess.PIPE).stdout.decode('utf-8')

	if audiofile in output:
		#print("file is playing")
		return True
	else:
		#print("file is not playing")
		return False

def record_story(figure):
	subprocess.Popen("AUDIODEV=hw:1 rec "+path+"figures/"+figure+"/"+figure+".mp3"+" ", shell=True, stdout=None, stderr=None)

	#TODO-maybe normalize, so volume boost at play_story can be removed -needs to be in other function because rec gets aborted
	#for example in the else block of stop_recording!
	#infile = path+"figures/"+folder+"/"+audiofile+".mp3"
	#outfile = path+"figures/"+folder+"/"+audiofile+"_normalized.mp3"
	#subprocess.Popen("sox --norm=-3 "+infile+" "+outfile+" 2>/dev/null",shell=True, stdout=None, stderr=None)
	#sox −−norm=−3 infile outfile

def stop_recording(figure_id):
	subprocess.Popen("killall rec",shell=True, stdout=None, stderr=None)

	figure_dir = path+"figures/"+figure_id

	#if file (koenigin.mp3 i.e.) exists (could not have been saved due to error in rec)
	if os.path.isfile(figure_dir+"/"+figure_id+".mp3"):
		#if file is smaller than 50kB, delete it
		if os.path.getsize(figure_dir+"/"+figure_id+".mp3") < 50000:
			os.remove(figure_dir+"/"+figure_id+".mp3")

			files_in_dir = os.listdir(figure_dir)

			#if directory is empty:
			if not files_in_dir:
				#delete the folder
				os.rmdir(figure_dir)

			#if not empty, meaning there is still one or more files (like koenigin2021-02-01-10-26.mp3)
			else:
				#rename the latest file back to koenigin.mp3 i.e.
				sorted_files = sorted(files_in_dir)
				os.rename(figure_dir+"/"+sorted_files[0],figure_dir+"/"+figure_id+".mp3")

			return True

	#if file does not exist
	else:
		files_in_dir = os.listdir(figure_dir)

		#if directory is empty (or if there is still a file like koenigin2021-02-01-10-26.mp3)
		if not files_in_dir:
			#delete the folder
			os.rmdir(figure_dir)

		#if not empty, meaning there is still one or more files (like koenigin2021-02-01-10-26.mp3)
		else:
			#rename the latest file back to koenigin.mp3 i.e.
			sorted_files = sorted(files_in_dir)
			os.rename(figure_dir+"/"+sorted_files[0],figure_dir+"/"+figure_id+".mp3")

		return True

def espeaker(words):
	os.system("espeak -v de+f2 -p 30 -g 12 -s 170 --stdout \""+str(words)+"\" | aplay -D 'default'")
	#espeak -v de+f2 -p 30 -g 12 -s 150 --stdout "apfelbaum" | aplay -D 'default'
