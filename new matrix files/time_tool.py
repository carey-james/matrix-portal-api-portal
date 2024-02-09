import time
from config import config

def time_tool(localtime):
	temp_min = localtime.tm_min
	if temp_min < 10:
		temp_min = '0' + str(temp_min)
	return f'{localtime.tm_hour}:{temp_min}'

def sleep_time_tool(localtime):
	if not config['sleep_timer']:
		return False
	temp_hour = localtime.tm_hour
	return (temp_hour >= config['sleep_time_start']) or (temp_hour < config['sleep_time_stop'])