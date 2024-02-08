import time
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import config

# --- Setup File Resources ---
# Current Working Directory
cwd = ('/' + __file__).rsplit('/', 1)[0]
# Weather icons spritesheet
weather_icon_spritesheet = cwd + '/weather-icons.bmp'
weather_icon_width = 16
weather_icon_height = 16



# --- Graphics Object Setup ---
class Graphics(displayio.Group):

	def __init__(self, display, *, am_pm=True):
		super().__init__()

		# Variables from Arguments
		self.am_pm = am_pm
		self.display = display

		# Setup the splash to display graphics
		splash = displayio.Group()

		# Setup Loading Splash, so we display something during rest of setup
		loading_background = displayio.OnDiskBitmap('loading.bmp', 'rb')
		loading_sprite = displayio.TileGrid(
			loading_background, 
			pixel_shader=loading_background.pixel_shader
			)
		splash.append(loading_sprite)

		# Setup the display groups
		self.root_group = displayio.Group()
		self.root_group.append(self)
		self._icon_group = displayio.Group()
		self.append(self._icon_group)
		self._text_group = displayio.Group()
		self.append(self._text_group)
		self._scrolling_group = displayio.Group()
		self.append(self._scrolling_group)

		# Load the weather icons sprite sheet
		weather_icons = displayio.OnDiskBitmap(icon_spritesheet)
		self._weather_icon_sprite = displayio.TileGrid(
			weather_icons, 
			pixel_shader=weather_icons.pixel_shader, 
			tile_width=weather_icon_width,
			tile_height=weather_icon_height
			)
		self.set_icon(None)

		# Setup the fonts
		self.small_font = bitmap_font.load_font(small_font)
        self.medium_font = bitmap_font.load_font(medium_font)
        glyphs = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: "
        self.small_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(("°",))  # non-ascii character

        # Setup the time text
        self.time_text = Label(self.medium_font)
        self.time_text.x = 16
        self.time_text.y = 7
        self.time_text.color = TIME_COLOR
        self._text_group.append(self.time_text)