import time
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from config import config

# --- Graphics Object Setup ---
class Graphics(displayio.Group):

	def __init__(self, display, *):
		super().__init__()

		# Variables from Arguments
		self.display = display

		# Setup File Resources
		# Current Working Directory
		cwd = ('/' + __file__).rsplit('/', 1)[0]

		# Setup the splash to display graphics
		splash = displayio.Group()

		# Setup Loading Splash, so we display something during rest of setup
		# Can all be local, because only used during this intial loading
		loading_background = displayio.OnDiskBitmap(config['loading_splash_path'])
		loading_sprite = displayio.TileGrid(
			loading_background, 
			pixel_shader=loading_background.pixel_shader
			)
		splash.append(loading_sprite)
		display.show(splash)

		# Setup the display groups
		self.root_group = displayio.Group()
		self.root_group.append(self)
		self._icon_group = displayio.Group()
		self.append(self._icon_group)
		self._text_group = displayio.Group()
		self.append(self._text_group)
		self._scrolling_group = displayio.Group()
		self.append(self._scrolling_group)

		# Setup the Sleep Splash for minimal display when the portal is in sleep state
		self.sleep_splash = displayio.Group()
		sleep_background = displayio.OnDiskBitmap(config['sleep_splash_path'])
		sleep_sprite = displayio.TileGrid(
			sleep_background,
			pixel_shader=sleep_background.pixel_shader
			)
		self.sleep_splash.append(sleep_sprite)

		# Load the weather icons sprite sheet
		weather_icons = displayio.OnDiskBitmap(cwd + config['weather_icon_spritesheet_path'])
		self._weather_icon_sprite = displayio.TileGrid(
			weather_icons, 
			pixel_shader=weather_icons.pixel_shader, 
			tile_width=config['weather_icon_width'],
			tile_height=config['weather_icon_height']
			)
		self.set_icon = None

		# Load the metro icons sprite sheet
		metro_icons = displayio.OnDiskBitmap(cwd + config['metro_icon_spritesheet_path'])
		self._metro_icon_sprite = displayio.TileGrid(
			metro_icons,
			pixel_shader=metro_icons.pixel_shader,
			tile_width=config['metro_icon_width'],
			tile_height=config['metro_icon_height']
			)

		# Load the spotify icons sprite sheet
		spotify_icons = displayio.OnDiskBitmap(cwd + config['spotify_icon_path'])
		self._spotify_icon_sprite = displayio.TileGrid(
			spotify_icons,
			pixel_shader=spotify_icons.pixel_shader,
			tile_width=config['spotify_icon_width'],
			tile_height=config['spotify_icon_height']
			)

		# Setup the fonts
		self.small_font = bitmap_font.load_font(cwd + config['small_font_path'])
		self.medium_font = bitmap_font.load_font(cwd + config['medium_font_path'])
		self.creep_font = bitmap_font.load_font(cwd + config['creep_font_path'])
		self.creep2_font = bitmap_font.load_font(cwd + config['creep2_font_path'])
		glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.:… '
		self.small_font.load_glyphs(glyphs)
		self.medium_font.load_glyphs(glyphs)
		self.creep_font.load_glyphs(glyphs)
		self.creep2_font.load_glyphs(glyphs)
		self.medium_font.load_glyphs(('°',))  # non-ascii character

		# Setup the time text
		self.am_pm = config['am_pm']
		self.time_text = Label(self.creep2_font)
		self.time_text.x = 36
		self.time_text.y = 4
		self.time_text.color = config['time_color']
		self._text_group.append(self.time_text)

		# Setting up message text
		self.message_text_1 = Label(self.creep2_font)
		self.message_text_1.x = 1
		self.message_text_1.y = 18
		self.message_text_1.color = config['time_color']
		self._text_group.append(self.message_text_1)
		self.message_text_2 = Label(self.creep2_font)
		self.message_text_2.x = 1
		self.message_text_2.y = 27
		self.message_text_2.color = config['time_color']
		self._text_group.append(self.message_text_2)

	# Used to update the Time display, unless it's sleep time
	def update_time(self, time, sleep_time):
		self.time_text.text = time
		if sleep_time:
			self.display.show(self.sleep_splash)
		else: self.display.show(self.root_group)

	# Used to set the current message for display, based on the message and icon provided		
	def display_message(self, message_ln_1, message_ln_2, icon_kind, icon_code):
		self.message_text_1.text = message_ln_1
		self.message_text_2.text = message_ln_2
		
		# Used to set the weather icon
		# Use weather_icon_name to update the current icon name,
		# based on the icon name returned by openweathermap
		# Format from openweathermap is 2 numbers followed by 'd' or 'n'
		if icon_kind == 'weather':
			if self._icon_group:
				self._icon_group.pop()
			if icon_code is not None:
				if icon_code[2] == 'n':
					column = 1
				else:
					column = 0
				for index, icon in enumerate(config['weather_icon_map']):
					# Index becomes row
					if icon == icon_code[0:2]:
						self._weather_icon_sprite[0] = (index * 2) + column
						self._icon_group.append(self._weather_icon_sprite)
						break

		elif icon_kind == 'metro':
			if self._icon_group:
				self._icon_group.pop()
			if icon_code is not None:
				if icon_code in config['metro_icon_map']:
					self._metro_icon_sprite[0] = config['metro_icon_map'][icon_code]
				else:
					self._metro_icon_sprite[0] = config['metro_icon_map']['PR']
				self._icon_group.append(self._metro_icon_sprite)

		elif icon_kind == 'spotify':
			if self._icon_group:
				self._icon_group.pop()
			if icon_code is not None:
				self._spotify_icon_sprite[0] = 0
				self._icon_group.append(self._spotify_icon_sprite)

		self.display.show(self.root_group)