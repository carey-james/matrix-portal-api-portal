import time
from config import config

def time_tool(localtime):
	temp_min = localtime.tm_min
	temp_hrs = localtime.tm_hour
	# Add padding 0s to minutes
	if temp_min < 10:
		temp_min = '0' + str(temp_min)
	# Set 24 hrs or 12 hr
	if config['am_pm']:
		temp_hrs = ((temp_hrs - 1) % 12) + 1
	temp_time = f'{temp_hrs}:{temp_min}'
	# Make nice Os instead of 0s if wanted
	if config['time_O']:
		temp_time = temp_time.replace('0','O')
	return temp_time

def sleep_time_tool(localtime):
	if not config['sleep_timer']:
		return False
	temp_hour = localtime.tm_hour
	return (temp_hour >= config['sleep_time_start']) or (temp_hour < config['sleep_time_stop'])