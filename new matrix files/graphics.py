import time
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from congfig import config

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

		# Setup the display groups
		self.root_group = displayio.Group()
		self.root_group.append(self)
		self._weather_icon_group = displayio.Group()
		self.append(self._weather_icon_group)
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
			tile_width=weather_icon_width,
			tile_height=weather_icon_height
			)
		self.set_icon(None)

		# Setup the fonts
		self.small_font = bitmap_font.load_font(cwd + config['small_font_path'])
	        self.medium_font = bitmap_font.load_font(cwd + config['medium_font_path'])
	        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
	        self.small_font.load_glyphs(glyphs)
	        self.medium_font.load_glyphs(glyphs)
	        self.medium_font.load_glyphs(("°",))  # non-ascii character
	
	        # Setup the time text
	        self.am_pm = config['am_pm']
	        self.time_text = Label(self.medium_font)
	        self.time_text.x = 16
	        self.time_text.y = 7
	        self.time_text.color = config['time_color']
	        self._text_group.append(self.time_text)

    # Used to update the Time display, unless it's sleep time
    def update_time(self, time, sleep_time):
    	self.time_text.text = time
    	if sleep_time:
    		self.display.show(self.sleep_splash)
    	else: self.display.show(self.root_group)

    # Used to set the weather icon
    # Use weather_icon_name to update the current icon name,
    # based on the icon name returned by openweathermap
    # Format from openweathermap is 2 numbers followed by 'd' or 'n'
    def set_weather_icon(self, weather_icon_name):
    	print(f'Setting weather icon to... {weather_icon_name}')
    	if self._weather_icon_group:
    		self._weather_icon_group.pop()
    	if weather_icon_name is not None:
    		column = 0
    		if icon_name[2] == 'n':
    			column = 1
    		for index, icon in enumerate(config['weather_icon_map']):
    			# Index becomes row
    			if icon == weather_icon_name[0:2]:
    				self._weather_icon_sprite[0] = (index * 2) + column
    				self._weather_icon_group.append(self._weather_icon_sprite)
    				break
