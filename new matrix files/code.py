import time
import board
import microcontroller
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

import graphics
from time_tool import time_tool, sleep_time_tool

from secrets import secrets
from config import config

# --- Matrix Setup ---
matrix = Matrix()

# --- Wifi Setup ---
# Network def
network = Network(status_neopixel=board.NEOPIXEL, debug=True)

# --- Display Setup ---
gfx = graphics.Graphics(matrix.display)

# --- Refresh Setup ---
localtime_refresh = None
weather_refresh = None

# --- Runner ---
while True:
	# --- Time Update ---
	# Only get the time from internet based on time_refresh_length and on startup
	if (not localtime_refresh) or ((time.monotonic() - localtime_refresh) > config['time_refresh_length_sec']):
		try:
			network.get_local_time()
			localtime_refresh = time.monotonic()
			# Use time_tool to update the time, 
			# and sleep_time_tool to see if we should be sleeping
			gfx.update_time(time_tool(time.localtime()), sleep_time_tool(time.localtime()))
		except RuntimeError as e:
			print(f'An error occured with the time! Retrying! {e}')
			continue

	# --- Weather Update --- 
	# Only get the weather every weather_refresh_length and on startup
	if (not weather_refresh) or ((time.monotonic() - weather_refresh) > config['weather_refresh_length_sec']):
		try:
			if not sleep_time_tool(time.localtime()):
				weather_response = network.fetch_data(f'{config['weather_source']}?q={config['weather_location']}&units={config['weather_units']}&appid={secrets['openweather_token']}', json_path=([]))
				gfx.set_weather_icon(weather_response['weather'][0]['icon'])
				weather_refresh = time.monotonic()
		except RuntimeError as e:
			print(f'An error occured with the weather! Retrying! {e}')
			continue

{'timezone': -28800, 
'sys': {'type': 2, 'sunrise': 1707664481, 'country': 'US', 'id': 2019804, 'sunset': 1707700677}, 
'base': 'stations', 
'main': {'pressure': 1018, 'feels_like': 38.41, 'temp_max': 42.33, 'temp': 38.41, 'temp_min': 36.48, 'humidity': 73, 'sea_level': 1018, 'grnd_level': 959}, 
'visibility': 39, 
'id': 5815135, 
'clouds': {'all': 100}, 
'coord': {'lon': -120.501, 'lat': 47.5001}, 
'name': 'Washington', 
'cod': 200, 
'weather': [{'id': 804, 'icon': '04d', 'main': 'Clouds', 'description': 'overcast clouds'}], 
'dt': 1707694085, 
'wind': {'gust': 2.68, 'speed': 2.95, 'deg': 80}}
