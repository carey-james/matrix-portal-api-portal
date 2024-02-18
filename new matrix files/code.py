import time
import board
import microcontroller
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

import graphics
from time_tool import time_tool, sleep_time_tool
from message_tool import message_tool, middle_pad, metro_no_psngr_check

from secrets import secrets
from config import config

# --- Matrix Setup ---
matrix = Matrix()

# --- Display Setup ---
gfx = graphics.Graphics(matrix.display)

# --- Wifi Setup ---
# Network def
network = Network(status_neopixel=board.NEOPIXEL, debug=True)

# --- Tokens Setup ---
# Setups for APIs which require tokens to be gotten/sent
# Spotify
spotify_token = ''
spotify_token_headers = {}
spotify_token_refresh_time = 0

# --- Message Stack Setup ---
# Message format:
# key = message type
# value =
# {
#	'message_ln_1': 12 character max,
#   'message_ln_2': 12 character max,
# 	'icon_kind':'weather' or 'other',
#   'icon_code': icon code 	
# }
message_stack = {}

# --- Stack Tracker Setup ---
# Used to manage where we are in the stack
stack_index = 0

# --- Refresh Setup ---
# These refresh vars show the last time that api was refreshed
localtime_refresh = None
weather_refresh = None
metro_refresh = None
message_refresh = None
spotify_refresh = None
spotify_token_refresh = None

# --- Runner ---
while True:
	# --- Time Update ---
	# Only get the time from internet based on time_refresh_length and on startup
	if (not localtime_refresh) or ((time.monotonic() - localtime_refresh) > config['time_refresh_length_sec']):
		try:
			network.get_local_time()
			localtime_refresh = time.monotonic()

		except RuntimeError as e:
			print(f'An error occured with the time! Retrying! {e}')
			continue

		except:
			print('Something else went wrong with the Time request...')
			continue
	# Use time_tool to update the time, 
	# and sleep_time_tool to see if we should be sleeping
	gfx.update_time(time_tool(time.localtime()), sleep_time_tool(time.localtime()))

	# --- Weather Update --- 
	# Only get the weather every weather_refresh_length and on startup
	if (not weather_refresh) or ((time.monotonic() - weather_refresh) > config['weather_refresh_length_sec']):
		try:
			if not sleep_time_tool(time.localtime()):
				# Get the weather
				weather_response = network.fetch_data(f'{config['weather_source']}?lat={secrets['lat']}&lon={secrets['lon']}&units={config['weather_units']}&appid={secrets['openweather_token']}', json_path=([]))
				cur_weather_icon_code = weather_response['weather'][0]['icon']
				
				# Add messages
				# Main weather
				message_stack['main_weather'] = {
					'message_ln_1':'Looking like', 
					'message_ln_2': message_tool(weather_response['weather'][0]['main']),
					'icon_kind':'weather',
					'icon_code': cur_weather_icon_code
				}
				# Cur Temp
				temp_temp = message_tool(weather_response['main']['temp']).split('.')[0]
				message_stack['weather_cur_temp'] = {
					'message_ln_1':'It\'s around', 
					'message_ln_2': f'{temp_temp}°F',
					'icon_kind':'weather',
					'icon_code': cur_weather_icon_code
				}

		except RuntimeError as e:
			print(f'An error occured with the weather! Try again later! {e}')
			pass

		except:
			print('Something else went wrong with the Weather request...')
			pass

		weather_refresh = time.monotonic()

	# --- Metro Update --- 
	# Only get the metro trains every metro_refresh_length and on startup
	if (not metro_refresh) or ((time.monotonic() - metro_refresh) > config['metro_refresh_length_sec']):
		try:
			if not sleep_time_tool(time.localtime()):
				# Get the status of each station
				for stat in config['metro_stations']:
					metro_response = list(network.fetch_data(f'{config['metro_source']}{config['metro_stations'][stat]}', headers={'api_key':secrets['metro_key']}, json_path=([]))['Trains'])
					print(metro_response)
					# Add Messages for the top two trains
					message_stack[f'{stat}'] = {
						'message_ln_1': middle_pad(metro_no_psngr_check(metro_response[0]['Destination']), metro_response[0]['Min']),
						'message_ln_2': middle_pad(metro_no_psngr_check(metro_response[1]['Destination']), metro_response[1]['Min']),
						'icon_kind':'metro',
						'icon_code': metro_response[0]['Line']
					}

		except RuntimeError as e:
			print(f'An error occured with the metro! Try again later! {e}')
			pass

		except:
			print('Something else went wrong with the Metro request...')
			pass

		metro_refresh = time.monotonic()

	# --- Spotify Token Update ---
	# Get the token from Spotify that will allow us to request data
	if (not spotify_token_refresh) or ((time.monotonic() - spotify_token_refresh) > spotify_token_refresh_time):
		try:
			spotify_token_response = network.fetch_data(config['spotify_token_source'], headers={'grant_type':'client_credentials', 'client_id': secrets['spotify_client_id'], 'client_secret': secrets['spotify_client_secret']}, json_path=([]))
			spotify_token = spotify_token_response['access_token']
			spotify_token_headers = {'Authorization': f'Bearer {spotify_token}'}
			spotify_token_refresh_time = spotify_token_response['expires in']
		
		except RuntimeError as e:
			print(f'An error occured with the Spotify token! Try again later! {e}')
			pass
		
		except:
			print('Something else went wrong with the Spotify token request...')
			pass

		spotify_token_refresh = time.monotonic()

	# --- Spotify Update ---
	# Update the Spotify playing data
	if (not spotify_refresh) or ((time.monotonic() - spotify_refresh) > config['spotify_refresh_length_sec']):
		try:
			spotify_playing_response = network.fetch_data(config['spotify_playing_source'], headers=spotify_token_headers, json_path=([]))
			if spotify_playing_response['currently_playing_type'] == 'track':
				# If it's a song, add a message for it in the format:
				# line 1: Song Name
				# line 2: Artist Name
				message_stack[f'{'spotify'}'] = {
					'message_ln_1': message_tool(spotify_playing_response['item']['name']),
					'message_ln_2': message_tool(spotify_playing_response['item']['artists'][0]['name']),
					'icon_kind':'spotify',
					'icon_code': 'song'
				}
			elif spotify_playing_response['currently_playing_type'] == 'episode':
				# If it's an episode, add a message for it in the format:
				# line 1: Episode Name
				# line 2: Show Name
				message_stack[f'{'spotify'}'] = {
					'message_ln_1': message_tool(spotify_playing_response['item']['name']),
					'message_ln_2': message_tool(spotify_playing_response['item']['show']['name']),
					'icon_kind':'spotify',
					'icon_code': 'pod'
				}
			else:
				del message_stack['spotify']

		except RuntimeError as e:
			print(f'An error occured with Spotify! Try again later! {e}')
			pass
		
		except:
			print('Something else went wrong with the Spotify request...')
			pass

		spotify_token = time.monotonic()

	# --- Message Update ---
	# Go through the message stack using the stack tracker, if we're gone to far, reset
	if (not message_refresh) or ((time.monotonic() - message_refresh) > config['message_refresh_length_sec']):
		if stack_index >= len(message_stack):
			stack_index = 0
		cur_message = message_stack[list(message_stack)[stack_index]]
		gfx.display_message(cur_message['message_ln_1'],cur_message['message_ln_2'],cur_message['icon_kind'],cur_message['icon_code'])
		stack_index += 1
		message_refresh = time.monotonic()
