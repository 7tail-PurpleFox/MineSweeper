import pyautogui
import sys
import os

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.normpath(os.path.join(base_path, relative_path))
MAX_WIDTH, MAX_HEIGHT = pyautogui.size()
SCREEN_SIZE = (552, 732)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
IMAGE_PATH = get_path('resource/image')
FONT_PATH = get_path('resource/font')
SOUND_PATH = get_path('resource/sound')
MUSIC_PATH = get_path('resource/music')

SETTING_PATH = '.minesweeper/game_setting.json'
RECORD_PATH = '.minesweeper/record'