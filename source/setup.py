import pygame
from . import constant as C
from . import tool

pygame.init()
screen = pygame.display.set_mode(C.SCREEN_SIZE, pygame.RESIZABLE)
screen.fill(C.BLACK)
pygame.display.set_caption('Mine Sweeper')
images = tool.load_image(C.IMAGE_PATH)
fonts_32 = tool.load_font(C.FONT_PATH,32)
fonts_24 = tool.load_font(C.FONT_PATH,24)
fonts_16 = tool.load_font(C.FONT_PATH,16)

border_hor_wide = images['border_hor_wide']
border_hor = images['border_hor']
border_vert = images['border_vert']
corner_bottom_left_wide = images['corner_bottom_left_wide']
corner_bottom_left = images['corner_bottom_left']
corner_bottom_right_wide = images['corner_bottom_right_wide']
corner_bottom_right = images['corner_bottom_right']
corner_up_left = images['corner_up_left']
corner_up_right = images['corner_up_right']
t_left = images["t_left"]
t_right = images["t_right"]
replay_cursor = images["replay_cursor"]
replay_play = images["replay_play"]
replay_start = images["replay_start"]
replay_previous = images["replay_previous"]
replay_next = images["replay_next"]
replay_end = images["replay_end"]
replay_pause = images["replay_pause"]
mouse_cursor = images["mouse_cursor"]

minecraft_font_32 = fonts_32['minecraft']
mine_sweeper_font_32 = fonts_32['mine_sweeper']
mine_sweeper_font_24 = fonts_24['mine_sweeper']
mine_sweeper_font_16 = fonts_16['mine_sweeper']

g = images['grid']
grids=[]
for i in range(0,256,16):
    temp=tool.get_image(g,0,i,16,16,scale=3)
    grids.insert(0,temp)

f = images["face"]
faces = []
for i in range(0,120,24):
    temp=tool.get_image(f,0,i,24,24,scale=3)
    faces.insert(0,temp)
    
n = images["number"]
numbers = []
for i in range(0,276,23):
    temp=tool.get_image(n,0,i,13,23,scale=3)
    numbers.insert(0,temp)

sounds = tool.load_sound(C.SOUND_PATH)
