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

minecraft_font_32 = fonts_32['minecraft']
mine_sweeper_font_32 = fonts_32['mine_sweeper']
mine_sweeper_font_24 = fonts_24['mine_sweeper']
mine_sweeper_font_16 = fonts_16['mine_sweeper']

g = images['grid']
grids=[]
for i in range(0,256,16):
    temp=tool.get_image(g,0,i,16,16,scale=3)
    grids.insert(0,temp)

sounds = tool.load_sound(C.SOUND_PATH)
