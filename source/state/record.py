import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Record:
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
        self.t_left = pygame.transform.scale(setup.t_left, (36,33))
        self.t_right = pygame.transform.scale(setup.t_right, (36,33))
        self.replay_cursor = pygame.transform.scale(setup.replay_cursor, (38,40))
        self.sound_explosion_1 = setup.sounds['explosion_1']
        self.sound_explosion_2 = setup.sounds['explosion_2']
        self.sound_button = setup.sounds['button']
        self.sound_click = setup.sounds["click"]
        self.sound_finish = setup.sounds["finish"]
        self.record_rect = pygame.Rect(36,33,480,96)
        self.last_game_rect = pygame.Rect(36,582,480,60)
        self.mine_rect = pygame.Rect(126,205,300,300)
        self.record=[]
        self.record_list=[]
        self.record_list_rect=[]
        self.slide_y=0
        self.slide_rect=pygame.Rect(26,680,500,23)
        self.cursor_rect=pygame.Rect(26,670,38,40)
        self.slide_check=False
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen,pos)
        sound_explosion = self.sound_explosion_1 if game_setting["explode_type"]==1 else self.sound_explosion_2
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(sound_explosion,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                temp=(387-len(self.record_list)*60)
                if event.y<0:
                    if temp<0:
                        self.slide_y-=20
                        if self.slide_y<temp:
                            self.slide_y=temp
                    else:
                        self.slide_y+=20
                        if self.slide_y>temp:
                            self.slide_y=temp
                else:
                    if temp<0:
                        self.slide_y+=20
                        if self.slide_y>0:
                            self.slide_y=0
                    else:
                        self.slide_y-=20
                        if self.slide_y<0:
                            self.slide_y=0
            elif event.type == pygame.MOUSEBUTTONUP:
                if not self.slide_check:
                    mine_check=True
                    if self.record_rect.collidepoint(pos):
                        self.sound_button.play()
                        self.finished = True
                        self.next = 'main_menu'
                    else:
                        for i in range(len(self.record_list_rect)):
                            rect=self.record_list_rect[i].copy()
                            rect.y+=self.slide_y
                            if rect.collidepoint(pos):
                                if rect.y<162:
                                    if rect.y+60>=162:
                                        if pos[1]>162:
                                            self.sound_button.play()
                                            self.finished = True
                                            self.next = 'record_info'
                                            mine_check=False
                                elif rect.y+60>549:
                                    if rect.y<=549:
                                        if pos[1]<549:
                                            self.sound_button.play()
                                            self.finished = True
                                            self.next = 'record_info'
                                            mine_check=False
                                else:
                                    self.sound_button.play()
                                    self.finished = True
                                    self.next = 'record_info'
                                    mine_check=False
                        if self.mine_rect.collidepoint(pos):
                            if mine_check:
                                sound_explosion.play()
                        
                self.slide_check=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.slide_rect.collidepoint(pos) or self.cursor_rect.collidepoint(pos):
                    self.slide_check=True
            
                
        if any(pygame.mouse.get_pressed()):
            if self.slide_check:
                temp=(387-len(self.record_list)*60)
                self.slide_y=temp*(pos[0]-46)/462
                if temp<0:
                    if self.slide_y<temp:
                        self.slide_y=temp
                    elif self.slide_y>0:
                        self.slide_y=0
                else:
                    if self.slide_y>temp:
                        self.slide_y=temp
                    elif self.slide_y<0:
                        self.slide_y=0
            elif self.last_game_rect.collidepoint(pos):
                temp = pygame.Surface((504,63))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Last Game',setup.mine_sweeper_font_24,2)
                temp = pygame.transform.scale(temp,(480,60))
                screen.blit(temp,self.last_game_rect.topleft)
            elif self.record_rect.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,'Record',setup.mine_sweeper_font_32,3)
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.record_rect.topleft)
            else:
                for i in range(len(self.record_list_rect)):
                    rect=self.record_list_rect[i].copy()
                    rect.y+=self.slide_y
                    if rect.collidepoint(pos):
                        temp = pygame.Surface((504,63))
                        temp.fill(C.GRAY)
                        self.blit_title(temp,self.record_list[i],setup.mine_sweeper_font_24,2)
                        temp = pygame.transform.scale(temp,(480,60))
                        if rect.y<162:
                            if rect.y+60>=162:
                                if pos[1]>162:
                                    screen.blit(tool.get_image(temp,0,162-(self.record_list_rect[i].topleft[1]+self.slide_y),480,self.record_list_rect[i].topleft[1]+self.slide_y+60-162),(self.record_list_rect[i].topleft[0],162))
                        elif rect.y+60>549:
                            if rect.y<=549:
                                if pos[1]<549:
                                    screen.blit(tool.get_image(temp,0,0,480,549-(self.record_list_rect[i].topleft[1]+self.slide_y)),(self.record_list_rect[i].topleft[0],self.record_list_rect[i].topleft[1]+self.slide_y))
                        else:
                            screen.blit(temp,rect.topleft)
                
    def set_backgroud(self,screen,pos):
        screen.blit(self.corner_up_left,(0,0))
        for i in range(36,516,6):
            screen.blit(self.border_hor,(i,0))
            screen.blit(self.border_hor,(i,129))
            screen.blit(self.border_hor,(i,549))
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
        screen.blit(self.t_left,(0,549))
        screen.blit(self.t_right,(516,549))
        temp = self.create_button_base()
        self.blit_title(temp,'Record',setup.mine_sweeper_font_32,3)
        screen.blit(temp,self.record_rect.topleft)
        
        temp=pygame.Surface((40,40))
        temp.fill(C.GRAY)
        self.blit_title(temp,'*',setup.mine_sweeper_font_16,1)
        temp=pygame.transform.scale(temp,(300,300))
        screen.blit(temp,self.mine_rect)
        check=True
        for i in self.record:
            if i[0]=="Last Game" and check:
                temp = self.create_sub_button_base()
                self.blit_title(temp,'Last Game',setup.mine_sweeper_font_24,2)
                screen.blit(temp,self.last_game_rect.topleft)
                check=False
        if check:
            temp=pygame.Surface((480,60))
            temp.fill(C.GRAY)
            self.blit_title(temp,"Just Explode A Mine !",setup.mine_sweeper_font_24,2)
            screen.blit(temp,self.last_game_rect.topleft)
        temp=pygame.Surface((500,23))
        temp.fill(C.DARK_GRAY)
        tool.blit_rectangle(temp,C.WHITE,(0,0),(497,20))
        screen.blit(temp,self.slide_rect.topleft)
        cord=self.slide_y/(387-len(self.record_list)*60)*462
        self.cursor_rect=pygame.Rect(cord+26,670,38,40)
        screen.blit(self.replay_cursor,self.cursor_rect.topleft)
        temp=pygame.Surface((10,20))
        temp.fill(C.GRAY)
        screen.blit(temp,(cord+34,680))
        for i in range(len(self.record_list)):
            temp = self.create_sub_button_base()
            self.blit_title(temp,self.record_list[i],setup.mine_sweeper_font_24,2)
            if self.record_list_rect[i].topleft[1]+self.slide_y<162:
                if self.record_list_rect[i].topleft[1]+self.slide_y+60>=162:
                    screen.blit(tool.get_image(temp,0,162-(self.record_list_rect[i].topleft[1]+self.slide_y),480,self.record_list_rect[i].topleft[1]+self.slide_y+60-162),(self.record_list_rect[i].topleft[0],162))
            elif self.record_list_rect[i].topleft[1]+self.slide_y+60>549:
                if self.record_list_rect[i].topleft[1]+self.slide_y<=549:
                    screen.blit(tool.get_image(temp,0,0,480,549-(self.record_list_rect[i].topleft[1]+self.slide_y)),(self.record_list_rect[i].topleft[0],self.record_list_rect[i].topleft[1]+self.slide_y))
            else:
                screen.blit(temp,(self.record_list_rect[i].topleft[0],self.record_list_rect[i].topleft[1]+self.slide_y))
        
                
                
        
        
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
    def blit_title(self,temp,text,font,frame):
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2+frame,temp.get_height()/2-frame),True)
        tool.blit_text(temp,font,text,C.WHITE,(temp.get_width()/2-frame,temp.get_height()/2+frame),True)
        tool.blit_text(temp,font,text,C.BLACK,(temp.get_width()/2,temp.get_height()/2),True)
    def get_record(self,record):
        self.record=record
        k=0
        self.record_list=[]
        self.record_list_rect=[]
        for i in record:
            if i[0]!="Last Game":
                self.record_list.append(i[0])
                self.record_list_rect.append(pygame.Rect(36,162+k*60,480,60))
                k+=1
        
    def create_sub_button_base(self):
        temp = pygame.Surface((480,60)).convert()
        temp2=pygame.Surface((48,24)).convert()
        temp2.blit(setup.grids[15],(0,-12))
        for i in range(0,480,48):
            temp.blit(setup.grids[15],(i,0))
            temp.blit(setup.grids[15],(i,12))
            temp.blit(temp2,(i,12))
        temp2=pygame.Surface((24,48)).convert()
        temp2.blit(setup.grids[15],(-12,0))
        for i in range(36,468,48):
            temp.blit(temp2,(i,0))
            temp.blit(temp2,(i,12))
            temp3=pygame.Surface((24,24)).convert()
            temp3.blit(setup.grids[15],(-12,-12))
            temp.blit(temp3,(i,12))
        return temp