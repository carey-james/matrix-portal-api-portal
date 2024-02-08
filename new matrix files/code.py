import graphics

import time
import board
import microcontroller
from digitalio import DigitalInOut, Direction, Pull
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

# --- Wifi Setup ---
# Get wifi details from secrets.py
try:
	from secrets import secrets
except ImportError:
	print('Please add a secrets.py file with your wifi secrets!')
	raise
# Network def
network = Network(status_neopixel=board.NEOPIXEL, debug=True)


# --- Display Setup ---
matrix = Matrix()
