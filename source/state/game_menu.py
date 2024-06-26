import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Game_Menu:
    def __init__(self):
        self.finished = False
        self.next = 'game_place'
        self.border_hor_wide = pygame.transform.scale(setup.border_hor_wide, ((6,90)))
        self.border_hor = pygame.transform.scale(setup.border_hor, ((6,33)))
        self.border_vert = pygame.transform.scale(setup.border_vert, ((36,6)))
        self.corner_bottom_left_wide = pygame.transform.scale(setup.corner_bottom_left_wide, (36,90))
        self.corner_bottom_left = pygame.transform.scale(setup.corner_bottom_left, (36,33))
        self.corner_bottom_right_wide = pygame.transform.scale(setup.corner_bottom_right_wide, (36,90))
        self.corner_bottom_right = pygame.transform.scale(setup.corner_bottom_right, (36,33))
        self.corner_up_left = pygame.transform.scale(setup.corner_up_left, (36,33))
        self.corner_up_right = pygame.transform.scale(setup.corner_up_right, (36,33))
        self.sound_button = setup.sounds['button']
        
        self.title = pygame.Rect(36,33,480,96)
        self.start = pygame.Rect(36,546,480,96)
        
        
        self.sub_titles = {"Beginner":[pygame.Rect(36,162,300,48),pygame.Rect(336,162,60,48),pygame.Rect(396,162,60,48),pygame.Rect(456,162,60,48)],
                           "Intermediate":[pygame.Rect(36,162,60,48),pygame.Rect(96,162,300,48),pygame.Rect(396,162,60,48),pygame.Rect(456,162,60,48)],
                           "Expert":[pygame.Rect(36,162,60,48),pygame.Rect(96,162,60,48),pygame.Rect(156,162,300,48),pygame.Rect(456,162,60,48)],
                           "Custom":[pygame.Rect(36,162,60,48),pygame.Rect(96,162,60,48),pygame.Rect(156,162,60,48),pygame.Rect(216,162,300,48)]}
        self.state = "Beginner"
        
        self.width = 9
        self.height = 9
        self.mines = 10
        
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen)
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.title.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    return "main_menu"
                elif self.sub_titles[self.state][0].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Beginner"
                elif self.sub_titles[self.state][1].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Intermediate"
                elif self.sub_titles[self.state][2].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Expert"
                elif self.sub_titles[self.state][3].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Custom"
    
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
        g=pygame.transform.scale(setup.grids[15],(30,30))
        temp=pygame.Surface((15,15)).convert()
        temp.blit(g,(-8,-8))
        temp2=pygame.Surface((15,15)).convert()
        temp2.blit(g,(0,-8))
        temp3=pygame.Surface((15,15)).convert()
        temp3.blit(g,(-15,-8))
        for i in range(210,546,15):
            for j in range(36,516,15):
                screen.blit(temp,(j,i))
            screen.blit(temp2,(36,i))
            screen.blit(temp3,(501,i))
        temp=pygame.Surface((15,15)).convert()
        temp.blit(g,(-8,-15))
        temp2=pygame.Surface((15,15)).convert()
        temp2.blit(g,(-8,0))
        for i in range(36,516,15):
            screen.blit(temp,(i,531))
            screen.blit(temp2,(i,210))
        temp=pygame.Surface((15,15)).convert()
        temp.blit(g,(0,-15))
        screen.blit(temp,(36,531))
        temp=pygame.Surface((15,15)).convert()
        temp.blit(g,(-15,-15))
        screen.blit(temp,(501,531))
        temp = pygame.Surface((15,15)).convert()
        temp.blit(g,(0,0))
        screen.blit(temp,(36,210))
        temp = pygame.Surface((15,15)).convert()
        temp.blit(g,(-15,0))
        screen.blit(temp,(501,210))
            
            
        temp = self.create_button_base()
        self.blit_title(temp,'Select Mode',setup.mine_sweeper_font_32,3)
        screen.blit(temp,self.title.topleft)
        temp = self.create_button_base()
        self.blit_title(temp,'Start',setup.mine_sweeper_font_32,3)
        screen.blit(temp,self.start.topleft)
        
        
        temp = self.create_sub_button_base()
        self.blit_title(temp,self.state,setup.mine_sweeper_font_16,2)
        temp2 = pygame.Surface((4,4)).convert()
        temp2.blit(g,(-26,0))
        temp2=pygame.transform.rotate(temp2,180)
        temp3 = self.create_dark_sub_button_base()

        if self.state == "Beginner":
            screen.blit(temp,self.sub_titles[self.state][0].topleft)
            screen.blit(temp2,(self.sub_titles[self.state][0].topleft[0]+297,self.sub_titles[self.state][0].topleft[1]+48))
            screen.blit(temp3,self.sub_titles[self.state][1].topleft)
            screen.blit(temp3,self.sub_titles[self.state][2].topleft)
            screen.blit(temp3,self.sub_titles[self.state][3].topleft)
        elif self.state == "Intermediate":
            screen.blit(temp3,self.sub_titles[self.state][0].topleft)
            screen.blit(temp,self.sub_titles[self.state][1].topleft)
            screen.blit(temp2,(self.sub_titles[self.state][1].topleft[0]+297,self.sub_titles[self.state][1].topleft[1]+48))
            screen.blit(temp3,self.sub_titles[self.state][2].topleft)
            screen.blit(temp3,self.sub_titles[self.state][3].topleft)
        elif self.state == "Expert":
            screen.blit(temp3,self.sub_titles[self.state][0].topleft)
            screen.blit(temp3,self.sub_titles[self.state][1].topleft)
            screen.blit(temp,self.sub_titles[self.state][2].topleft)
            screen.blit(temp2,(self.sub_titles[self.state][2].topleft[0]+297,self.sub_titles[self.state][2].topleft[1]+48))
            screen.blit(temp3,self.sub_titles[self.state][3].topleft)
        elif self.state == "Custom":
            screen.blit(temp3,self.sub_titles[self.state][0].topleft)
            screen.blit(temp3,self.sub_titles[self.state][1].topleft)
            screen.blit(temp3,self.sub_titles[self.state][2].topleft)
            screen.blit(temp,self.sub_titles[self.state][3].topleft)
        
        
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
    def create_sub_button_base(self):
        temp = pygame.Surface((300,52)).convert()
        g=pygame.transform.scale(setup.grids[15],(30,30))
        temp2=pygame.Surface((30,15)).convert()
        temp2.blit(g,(0,-8))
        for i in range(0,300,30):
            temp.blit(g,(i,0))
            temp.blit(g,(i,26))
            temp.blit(temp2,(i,18))
        temp2=pygame.Surface((15,30)).convert()
        temp2.blit(g,(-8,0))
        for i in range(9):
            a=22+i*30
            temp.blit(temp2,(a,0))
            temp.blit(temp2,(a,26))
            temp3=pygame.Surface((15,15)).convert()
            temp3.blit(g,(-8,-8))
            temp.blit(temp3,(a,18))
        return temp
    def create_dark_sub_button_base(self):
        temp = pygame.Surface((60,48)).convert()
        g=pygame.transform.scale(setup.grids[15],(30,30))
        temp2=pygame.Surface((30,15)).convert()
        temp2.blit(g,(0,-8))
        for i in range(0,60,30):
            temp.blit(g,(i,0))
            temp.blit(g,(i,18))
            temp.blit(temp2,(i,18))
        temp2=pygame.Surface((15,30)).convert()
        temp2.blit(g,(-8,0))
        for i in range(1):
            a=22+i*30
            temp.blit(temp2,(a,0))
            temp.blit(temp2,(a,18))
            temp3=pygame.Surface((15,15)).convert()
            temp3.blit(g,(-8,-8))
            temp.blit(temp3,(a,18))
        tool.blit_text(temp,setup.mine_sweeper_font_16,'*',C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
        temp4=pygame.Surface((60,48)).convert()
        temp4.fill(C.BLACK)
        temp4.set_alpha(100)
        temp.blit(temp4,(0,0))
        return temp
    def blit_title(self,temp,text,font,frame):
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)