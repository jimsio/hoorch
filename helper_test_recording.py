"""
This helper records 10 seconds of audio
switches amp off before recording and switches it on afterwards for playing the file
"""

import time
import digitalio
import board
import subprocess
import os

#speaker cracks when recording starts

def main():
        #set environment variable for sox rec
        os.environ['AUDIODRIVER'] = "alsa"

        amp_sd = digitalio.DigitalInOut(board.D6)
        amp_sd.direction = digitalio.Direction.OUTPUT

        print("switching off amp - volt should be 0")
        amp_sd.value = False
        time.sleep(1)

        print("start recording 10 seconds of audio")
        subprocess.Popen("AUDIODEV=dmic_sv rec -c 1 rectest.mp3", shell=True, stdout=None, stderr=None)
        time.sleep(10)
        subprocess.Popen("killall rec",shell=True, stdout=None, stderr=None)

        print("finished recording, trim of the first 0.3 seconds")
        subprocess.Popen("sox rectest.mp3 trimmed.mp3 trim 0.3", shell=True, stdout=None, stderr=None)

        print("swithing on amp - volt on SD pin should be 3.3 V")
        amp_sd.value = True
        print("play the file rectest.mp3 - should be a crack at the beginning")

        subprocess.Popen("play rectest.mp3",shell=True, stdout=None, stderr=None)
        time.sleep(12)
        print("play file trimmed - without the clicking; right?")
        subprocess.Popen("play trimmed.mp3", shell=True, stdout=None, stderr=None)
        time.sleep(12)

        #print("switching off the amp - volt should be 0 V")
        #amp_sd.value = False

        print("done with the script. goodbye")


if __name__ == "__main__":
        main()