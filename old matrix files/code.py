# The Main code.py file for the Matrix Portal API Portal

import os
import json
import time
import board
import microcontroller

from digitalio import DigitalInOut, Direction, Pull
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

# Import config 
import config

# Get wifi details and API info from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Get board json configs, load them into a list to cycle through
boards_json_list = []
board_files_list = os.listdir('./boards')
for bf in board_files_list:
    if bf.endswith('.json'):
        boards_list.append(json.loads(read(open(bf,'r'))))

if hasattr(board, "D12"):
    jumper = DigitalInOut(board.D12)
    jumper.direction = Direction.INPUT
    jumper.pull = Pull.UP
    is_metric = jumper.value
elif hasattr(board, "BUTTON_DOWN") and hasattr(board, "BUTTON_UP"):
    button_down = DigitalInOut(board.BUTTON_DOWN)
    button_down.switch_to_input(pull=Pull.UP)

    button_up = DigitalInOut(board.BUTTON_UP)
    button_up.switch_to_input(pull=Pull.UP)
    if not button_down.value:
        print("Down Button Pressed")
        microcontroller.nvm[0] = 1
    elif not button_up.value:
        print("Up Button Pressed")
        microcontroller.nvm[0] = 0
    print(microcontroller.nvm[0])
    is_metric = microcontroller.nvm[0]
else:
    is_metric = False

if is_metric:
    UNITS = "metric"  # can pick 'imperial' or 'metric' as part of URL query
    print("Jumper set to metric")
else:
    UNITS = "imperial"
    print("Jumper set to imperial")

# Use cityname, country code where countrycode is ISO3166 format.
# E.g. "New York, US" or "London, GB"
LOCATION = "Petaluma, US"
print("Getting weather for {}".format(LOCATION))
# Set up from where we'll be fetching data
DATA_SOURCE = (
    "http://api.openweathermap.org/data/2.5/weather?q=" + LOCATION + "&units=" + UNITS
)
DATA_SOURCE += "&appid=" + secrets["openweather_token"]
AQI_SOURCE = "https://www.purpleair.com/json?show=" + secrets["aqi_sensor"]
# You'll need to get a token from openweather.org, looks like 'b6907d289e10d714a6e88b30761fae22'
# it goes in your secrets.py file on a line such as:
# 'openweather_token' : 'your_big_humongous_gigantor_token',
DATA_LOCATION = []
SCROLL_HOLD_TIME = 0  # set this to hold each line before finishing scroll

# Display Setup
matrix = Matrix()
network = Network(status_neopixel=board.NEOPIXEL, debug=True)
if UNITS in ("imperial", "metric"):
    gfx = openweather_graphics.OpenWeather_Graphics(
        matrix.display, am_pm=True, units=UNITS
    )

print("gfx loaded")
localtime_refresh = None
weather_refresh = None

# The Running Loop
while True:
    # only query the online time once per hour (and on first run)
    if (not localtime_refresh) or (time.monotonic() - localtime_refresh) > 3600:
        try:
            print("Getting time from internet!")
            network.get_local_time()
            localtime_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # only query the weather every 10 minutes (and on first run)
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600:
        try:
            value = network.fetch_data(DATA_SOURCE, json_path=(DATA_LOCATION,))
            # aqi_value = purple_aqi.aqi_transform(network.fetch_data(AQI_SOURCE, json_path=(["results", 0, "PM2_5Value"],["results", 0, "PM2_5Value"]))[0])
            print("Weather response is", value)
            # print("AQI reponse is", aqi_value)
            aqi_value = 0
            gfx.display_weather(value, aqi_value)
            weather_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    
    temp_min = time.localtime().tm_min
    if temp_min < 10:
        temp_min = '0' + str(temp_min)  
    temp_time = f'{time.localtime().tm_hour}:{temp_min}'
    gfx.update_time(temp_time)
    gfx.scroll_next_label()
    # Pause between labels
    time.sleep(SCROLL_HOLD_TIME)