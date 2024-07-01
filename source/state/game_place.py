import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Game_Place:
    def __init__(self):
        self.finished = False
        self.next = 'main_menu'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.sound_explosion_1 = setup.sounds['explosion_1']
        self.sound_explosion_2 = setup.sounds['explosion_2']
        self.sound_button = setup.sounds['button']
        
    def update(self,screen,events,pos,game_setting):
        width=game_setting["game_place"][0]
        height=game_setting["game_place"][1]
        mines=game_setting["game_place"][2]
        self.set_backgroud(screen,width,height,mines)
        temp=pygame.Surface((10,10))
        screen.blit(temp,pos)
        
    
    def set_backgroud(self,screen,width,height,mines):
        screen.blit(self.corner_up_left,(0,0))
        for i in range(36,516,6):
            screen.blit(self.border_hor,(i,0))
            screen.blit(self.border_hor,(i,129))
            screen.blit(self.border_hor_wide,(i,642))
        screen.blit(self.corner_up_right,(516,0))
        screen.blit(self.corner_bottom_left_wide,(0,642))
        screen.blit(self.corner_bottom_right_wide,(516,642))
        for i in range(33,129,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(516,i))
        screen.blit(self.corner_bottom_left,(0,129))
        screen.blit(self.corner_bottom_right,(516,129))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_left,(0,-17))
        screen.blit(temp,(0,146))
        temp = pygame.Surface((36,16)).convert()
        temp.blit(self.corner_up_right,(0,-17))
        screen.blit(temp,(516,146))
        for i in range(162,642,6):
            screen.blit(self.border_vert,(0,i))
            screen.blit(self.border_vert,(516,i))