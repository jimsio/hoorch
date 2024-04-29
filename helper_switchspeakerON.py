"""
This helper switches the amp on, helpful for testing
"""
import time
import digitalio
import board
import subprocess
import os

def main():
    amp_sd = digitalio.DigitalInOut(board.D6) #GPIO6
    amp_sd.direction = digitalio.Direction.OUTPUT

    print("switching ON amp - volt on SD pin on amp should be 3.3")
    amp_sd.value = True
    time.sleep(1)


if __name__ == "__main__":
    main()