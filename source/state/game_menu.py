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
        
        self.custom_field_frame = [pygame.Rect(300,271,150,50),pygame.Rect(300,341,150,50),pygame.Rect(300,411,150,50)]
        self.custom_field_activate = [False,False,False]
        self.start_check = False
        self.custom_reset_rect = pygame.Rect(126,482,300,48)
        self.key_check=False
        
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen)
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if not (self.custom_field_frame[0].collidepoint(pos) or self.custom_field_frame[1].collidepoint(pos) or self.custom_field_frame[2].collidepoint(pos)):
                    self.custom_field_activate = [False,False,False]
                    self.key_check=False
                if self.title.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = "main_menu"
                elif self.sub_titles[self.state][0].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Beginner"
                    self.width = 9
                    self.height = 9
                    self.mines = 10
                elif self.sub_titles[self.state][1].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Intermediate"
                    self.width = 16
                    self.height = 16
                    self.mines = 40
                elif self.sub_titles[self.state][2].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Expert"
                    self.width = 30
                    self.height = 16
                    self.mines = 99
                elif self.sub_titles[self.state][3].collidepoint(pos):
                    self.sound_button.play()
                    self.state = "Custom"
                    self.width = game_setting["custom_field"][0]
                    self.height = game_setting["custom_field"][1]
                    self.mines = game_setting["custom_field"][2]
                elif self.custom_field_frame[0].collidepoint(pos):
                    if self.custom_field_activate[0]:
                        self.width = 0
                    else:
                        self.custom_field_activate=[False,False,False]
                        self.custom_field_activate[0] = True
                        self.key_check=False
                elif self.custom_field_frame[1].collidepoint(pos):
                    if self.custom_field_activate[1]:
                        self.height = 0
                    else:
                        self.custom_field_activate=[False,False,False]
                        self.custom_field_activate[1] = True
                        self.key_check=False
                elif self.custom_field_frame[2].collidepoint(pos):
                    if self.custom_field_activate[2]:
                        self.mines = 0
                    else:
                        self.custom_field_activate=[False,False,False]
                        self.custom_field_activate[2] = True
                        self.key_check=False
                elif self.custom_reset_rect.collidepoint(pos):
                    if self.state=="Custom":
                        self.sound_button.play()
                        self.width = 0
                        self.height = 0
                        self.mines = 0
                        return "custom_field."+str(self.width)+" "+str(self.height)+" "+str(self.mines)
                elif self.start.collidepoint(pos):
                    if self.start_check:
                        self.sound_button.play()
                        self.finished = True
                        self.next = "game_place"
                        return "game_places."+str(self.width)+" "+str(self.height)+" "+str(self.mines)
            elif event.type == pygame.KEYDOWN:
                if self.state == "Custom":
                    check = False
                    temp=0
                    for i in range(3):
                        if self.custom_field_activate[i]:
                            
                            if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                                self.custom_field_activate[i] = False
                                if not check:
                                    temp = (i+1)%3
                                    check = True
                                    self.key_check=False
                            elif event.key == pygame.K_UP:
                                if i == 0:
                                    self.width = self.width if self.width == 99 else self.width+1
                                elif i == 1:
                                    self.height = self.height if self.height == 99 else self.height+1
                                elif i == 2:
                                    self.mines = self.mines if self.mines == 9999 else self.mines+1
                                self.key_check=False
                                return "custom_field."+str(self.width)+" "+str(self.height)+" "+str(self.mines)
                            elif event.key == pygame.K_DOWN:
                                if i == 0:
                                    self.width = self.width if self.width == 0 else self.width-1
                                elif i == 1:
                                    self.height = self.height if self.height == 0 else self.height-1
                                elif i == 2:
                                    self.mines = self.mines if self.mines == 0 else self.mines-1
                                self.key_check=False
                                return "custom_field."+str(self.width)+" "+str(self.height)+" "+str(self.mines)
                            elif event.key == pygame.K_BACKSPACE:
                                if i == 0:
                                    self.width = 0 if len(str(self.width)) == 1 else int(str(self.width)[:-1])
                                elif i == 1:
                                    self.height = 0 if len(str(self.height)) == 1 else int(str(self.height)[:-1])
                                elif i == 2:
                                    self.mines = 0 if len(str(self.mines)) == 1 else int(str(self.mines)[:-1])
                                return "custom_field."+str(self.width)+" "+str(self.height)+" "+str(self.mines)
                            elif event.key in range(48,58):
                                if self.key_check:
                                    if i == 0:
                                        self.width = self.width if len(str(self.width)) == 2 else int(str(self.width)+chr(event.key))
                                    elif i == 1:
                                        self.height = self.height if len(str(self.height)) == 2 else int(str(self.height)+chr(event.key))
                                    elif i == 2:
                                        self.mines = self.mines if len(str(self.mines)) == 4 else int(str(self.mines)+chr(event.key))
                                else:
                                    if i == 0:
                                        self.width = int(chr(event.key))
                                    elif i == 1:
                                        self.height = int(chr(event.key))
                                    elif i == 2:
                                        self.mines = int(chr(event.key))
                                    self.key_check=True
                                return "custom_field "+str(self.width)+" "+str(self.height)+" "+str(self.mines)
                    if check:
                        self.custom_field_activate[temp] = True
        if any(pygame.mouse.get_pressed()):
            if self.title.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Select Mode',setup.mine_sweeper_font_32,3)
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.title.topleft)
            elif self.start.collidepoint(pos):
                if self.start_check:
                    temp = pygame.Surface((500,100))
                    temp.fill(C.GRAY)
                    self.blit_title(temp,'Start',setup.mine_sweeper_font_32,3)
                    temp = pygame.transform.scale(temp,(480,96))
                    screen.blit(temp,self.start.topleft)
            elif self.sub_titles[self.state][0].collidepoint(pos):
                if self.sub_titles[self.state][0].width==60:
                    temp = pygame.Surface((65,52))
                    temp.fill(C.GRAY)
                    tool.blit_text(temp,setup.mine_sweeper_font_16,'*',C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
                    temp = pygame.transform.scale(temp,(60,48))
                    temp2=pygame.Surface((60,48)).convert()
                    temp2.fill(C.BLACK)
                    temp2.set_alpha(100)
                    temp.blit(temp2,(0,0))
                    screen.blit(temp,self.sub_titles[self.state][0].topleft)
                    
            elif self.sub_titles[self.state][1].collidepoint(pos):
                if self.sub_titles[self.state][1].width==60:
                    temp = pygame.Surface((65,52))
                    temp.fill(C.GRAY)
                    tool.blit_text(temp,setup.mine_sweeper_font_16,'*',C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
                    temp = pygame.transform.scale(temp,(60,48))
                    temp2=pygame.Surface((60,48)).convert()
                    temp2.fill(C.BLACK)
                    temp2.set_alpha(100)
                    temp.blit(temp2,(0,0))
                    screen.blit(temp,self.sub_titles[self.state][1].topleft)
            elif self.sub_titles[self.state][2].collidepoint(pos):
                if self.sub_titles[self.state][2].width==60:
                    temp = pygame.Surface((65,52))
                    temp.fill(C.GRAY)
                    tool.blit_text(temp,setup.mine_sweeper_font_16,'*',C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
                    temp = pygame.transform.scale(temp,(60,48))
                    temp2=pygame.Surface((60,48)).convert()
                    temp2.fill(C.BLACK)
                    temp2.set_alpha(100)
                    temp.blit(temp2,(0,0))
                    screen.blit(temp,self.sub_titles[self.state][2].topleft)
            elif self.sub_titles[self.state][3].collidepoint(pos):
                if self.sub_titles[self.state][3].width==60:
                    temp = pygame.Surface((65,52))
                    temp.fill(C.GRAY)
                    tool.blit_text(temp,setup.mine_sweeper_font_16,'*',C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
                    temp = pygame.transform.scale(temp,(60,48))
                    temp2=pygame.Surface((60,48)).convert()
                    temp2.fill(C.BLACK)
                    temp2.set_alpha(100)
                    temp.blit(temp2,(0,0))
                    screen.blit(temp,self.sub_titles[self.state][3].topleft)
            elif self.custom_reset_rect.collidepoint(pos):
                    if self.state=="Custom":
                        temp = pygame.Surface((325,52))
                        temp.fill(C.GRAY)
                        self.blit_title(temp,'Reset',setup.mine_sweeper_font_16,2)
                        temp = pygame.transform.scale(temp,(300,48))
                        screen.blit(temp,self.custom_reset_rect.topleft)
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
        if self.state != "Custom":
            temp = self.create_button_base()
            self.blit_title(temp,'Start',setup.mine_sweeper_font_32,3)
            screen.blit(temp,self.start.topleft)
        
        
        temp = self.create_sub_button_base()
        self.blit_title(temp,self.state,setup.mine_sweeper_font_16,2)
        temp2 = pygame.Surface((4,4)).convert()
        temp2.blit(g,(-26,0))
        temp2=pygame.transform.rotate(temp2,180)
        temp3 = self.create_dark_sub_button_base()
        self.start_check = False if self.state == "Custom" else True
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
        
        if self.state == "Custom":
            for j in range(3):
                i = self.custom_field_frame[j]
                if self.custom_field_activate[j]:
                    tool.blit_rectangle(screen,C.WHITE,i.topleft,i.size)
                else:
                    tool.blit_rectangle(screen,(150,150,150),i.topleft,i.size)
                tool.blit_rectangle(screen,C.GRAY,(i.topleft[0]+5,i.topleft[1]+5),(i.size[0]-10,i.size[1]-10))
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.width),C.WHITE,(375+3,296+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.width),C.WHITE,(375-3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.width),C.WHITE,(375+3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.width),C.WHITE,(375-3,296+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.width),C.BLACK,(375,296),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.height),C.WHITE,(375+3,366+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.height),C.WHITE,(375-3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.height),C.WHITE,(375+3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.height),C.WHITE,(375-3,366+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.height),C.BLACK,(375,366),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.mines),C.WHITE,(375+3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.mines),C.WHITE,(375-3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.mines),C.WHITE,(375+3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.mines),C.WHITE,(375-3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,str(self.mines),C.BLACK,(375,436),True)            
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width :',C.WHITE,(200+3,296+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width :',C.WHITE,(200-3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width :',C.WHITE,(200+3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width :',C.WHITE,(200-3,296+3),True)        
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width :',C.BLACK,(200,296),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height :',C.WHITE,(200+3,366+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height :',C.WHITE,(200-3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height :',C.WHITE,(200+3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height :',C.WHITE,(200-3,366+3),True)        
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height :',C.BLACK,(200,366),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines :',C.WHITE,(200+3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines :',C.WHITE,(200-3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines :',C.WHITE,(200+3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines :',C.WHITE,(200-3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines :',C.BLACK,(200,436),True)
            text=''
            temp = self.create_sub_button_base_2()
            self.blit_title(temp,'Reset',setup.mine_sweeper_font_16,2)
            screen.blit(temp,self.custom_reset_rect.topleft)
            if self.width <= 0:
                text='Width must be greater than 0'
            elif self.height <= 0:
                text='Height must be greater than 0'
            elif self.mines > self.width*self.height:
                text='Mines must be less than '+str(self.width*self.height)
            elif self.state=="Custom":
                self.start_check = True
            if self.start_check:
                temp = self.create_button_base()
                self.blit_title(temp,'Start',setup.mine_sweeper_font_32,3)
                screen.blit(temp,self.start.topleft)
            else:
                temp = pygame.Surface((480,96)).convert()
                temp.fill(C.GRAY)
                self.blit_title(temp,text,setup.mine_sweeper_font_16,3)
                screen.blit(temp,self.start.topleft)
        else:
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width : '+str(self.width),C.WHITE,(276+3,296+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width : '+str(self.width),C.WHITE,(276-3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width : '+str(self.width),C.WHITE,(276+3,296-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width : '+str(self.width),C.WHITE,(276-3,296+3),True)        
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Width : '+str(self.width),C.BLACK,(276,296),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height : '+str(self.height),C.WHITE,(276+3,366+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height : '+str(self.height),C.WHITE,(276-3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height : '+str(self.height),C.WHITE,(276+3,366-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height : '+str(self.height),C.WHITE,(276-3,366+3),True)        
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Height : '+str(self.height),C.BLACK,(276,366),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines : '+str(self.mines),C.WHITE,(276+3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines : '+str(self.mines),C.WHITE,(276-3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines : '+str(self.mines),C.WHITE,(276+3,436-3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines : '+str(self.mines),C.WHITE,(276-3,436+3),True)
            tool.blit_text(screen,setup.mine_sweeper_font_24,'Mines : '+str(self.mines),C.BLACK,(276,436),True)
        
        
        
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
    def create_sub_button_base_2(self):
        temp = pygame.Surface((300,48)).convert()
        g=pygame.transform.scale(setup.grids[15],(30,30))
        temp2=pygame.Surface((30,15)).convert()
        temp2.blit(g,(0,-8))
        for i in range(0,300,30):
            temp.blit(g,(i,0))
            temp.blit(g,(i,18))
            temp.blit(temp2,(i,18))
        temp2=pygame.Surface((15,30)).convert()
        temp2.blit(g,(-8,0))
        for i in range(9):
            a=22+i*30
            temp.blit(temp2,(a,0))
            temp.blit(temp2,(a,18))
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