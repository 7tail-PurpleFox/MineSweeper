import pygame
from .. import setup
from .. import constant as C
from .. import tool

class MainMenu:
    def __init__(self):
        self.finished = False
        self.next = 'game_menu'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.sound_explosion = setup.explosion_sounds[0]
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.click_sounds[0]
        self.sound_finish = setup.sounds["finish"]

        self.title = pygame.Rect(36,33,480,96)
        self.new_game = pygame.Rect(36,162,480,96)
        self.record = pygame.Rect(36,258,480,96)
        self.options = pygame.Rect(36,354,480,96)
        self.tutorial = pygame.Rect(36,450,480,96)
        self.exit = pygame.Rect(36,546,480,96)
        self.button_enable=True
        
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen)
        self.sound_explosion = setup.explosion_sounds[game_setting["explode_type"]-1]
        self.sound_click = setup.click_sounds[game_setting["click_type"]-1]
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_explosion,game_setting["explode_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.button_enable:
                if self.new_game.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = "game_menu"
                elif self.record.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = "record"
                elif self.options.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = "options"
                elif self.tutorial.collidepoint(pos):
                    self.sound_button.play()
                elif self.exit.collidepoint(pos):
                    return "quit"
                elif self.title.collidepoint(pos):
                    self.sound_explosion.play()
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.new_game.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'New Game')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.new_game.topleft)
            elif self.record.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Record')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.record.topleft)
            elif self.options.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Options')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.options.topleft)
            elif self.tutorial.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Tutorial')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.tutorial.topleft)
            elif self.exit.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Exit')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.exit.topleft)
            elif self.title.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Mine*Sweeper')
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.title.topleft)
                

        
    
    def set_backgroud(self,screen):
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
        
        temp = self.create_button_base()
        self.blit_title(temp,'Mine*Sweeper')
        screen.blit(temp,self.title.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'New Game')
        screen.blit(temp,self.new_game.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'Record')
        screen.blit(temp,self.record.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'Options')
        screen.blit(temp,self.options.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'Tutorial')
        screen.blit(temp,self.tutorial.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'Exit')
        screen.blit(temp,self.exit.topleft)
        
    def create_button_base(self):
        temp = pygame.Surface((480,96)).convert()
        temp2=pygame.Surface((48,24)).convert()
        temp2.blit(setup.grids[15],(0,-12))
        for i in range(0,480,48):
            temp.blit(setup.grids[15],(i,0))
            temp.blit(setup.grids[15],(i,48))
            temp.blit(temp2,(i,36))
        temp2=pygame.Surface((24,48)).convert()
        temp2.blit(setup.grids[15],(-12,0))
        for i in range(36,468,48):
            temp.blit(temp2,(i,0))
            temp.blit(temp2,(i,48))
            temp3=pygame.Surface((24,24)).convert()
            temp3.blit(setup.grids[15],(-12,-12))
            temp.blit(temp3,(i,36))
        return temp
    def blit_title(self,temp,text):
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2+3,temp.get_height()/2-3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.WHITE,(temp.get_width()/2-3,temp.get_height()/2+3),True)
        tool.blit_text(temp,setup.mine_sweeper_font_32,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)