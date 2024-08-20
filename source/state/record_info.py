import pygame
from .. import setup
from .. import constant as C
from .. import tool

class Record_Info:
    def __init__(self):
        self.finished = False
        self.next = 'record'
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
        self.title_rect = pygame.Rect(36,33,480,96)
        self.record = {}
        self.record_info = ""
        self.button_enable=True
        self.bv = 0
    def update(self,screen,events,pos,game_setting):
        self.set_backgroud(screen,pos)
        sound_explosion = self.sound_explosion_1 if game_setting["explode_type"]==1 else self.sound_explosion_2
        pygame.mixer.Sound.set_volume(self.sound_button,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(sound_explosion,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_click,game_setting["sound_scale"]/10)
        pygame.mixer.Sound.set_volume(self.sound_finish,game_setting["sound_scale"]/10)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.button_enable:
                if self.title_rect.collidepoint(pos):
                    self.sound_button.play()
                    self.finished = True
                    self.next = 'record'
                
        self.button_enable=False
        if any(pygame.mouse.get_pressed()):
            self.button_enable=True
            if self.title_rect.collidepoint(pos):
                temp = pygame.Surface((500,100))
                temp.fill(C.GRAY)
                self.blit_title(temp,self.record_info,setup.mine_sweeper_font_32,3)
                temp = pygame.transform.scale(temp,(480,96))
                screen.blit(temp,self.title_rect.topleft)
            
    def set_backgroud(self,screen,pos):
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

        temp = pygame.Surface((48,24)).convert()
        temp.blit(setup.grids[15],(0,-12))
        for i in range(0,480,48):
            for j in range(162,642,48):
                screen.blit(setup.grids[15],(i+36,j))
            for j in range(210,642,48):
                screen.blit(temp,(i+36,j-12))
        
        temp=pygame.Surface((24,48)).convert()
        temp.blit(setup.grids[15],(-12,0))
        for i in range(36,468,48):
            for j in range(162,642,48):
                screen.blit(temp,(i+36,j))
            temp3=pygame.Surface((24,24)).convert()
            temp3.blit(setup.grids[15],(-12,-12))
            for j in range(210,642,48):
                screen.blit(temp3,(i+36,j-12))

        temp = self.create_button_base()
        self.blit_title(temp,self.record_info,setup.mine_sweeper_font_32,3)
        screen.blit(temp,self.title_rect.topleft)

        self.blit_title2(screen,setup.mine_sweeper_font_16,"Record Name : "+self.record_info,C.BLACK,(276,200),2,C.WHITE,True)
        temp = self.record["date"].split(" ")
        temp = temp[0]+"/"+temp[1]+"/"+temp[2]+" "+temp[3]+":"+temp[4]+":"+temp[5]
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Date : "+temp,C.BLACK,(276,250),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Result : "+self.record["result"],C.BLACK,(276,300),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Width : "+str(self.record["width"])+"  Height : "+str(self.record["height"]),C.BLACK,(276,350),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Mines : "+str(self.record["mines"])+"  3BV : "+str(self.bv),C.BLACK,(276,400),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"Time : "+str(self.record["gaming"][-1]["time"]/1000)+" Second",C.BLACK,(276,450),2,C.WHITE,True)
        self.blit_title2(screen,setup.mine_sweeper_font_16,"3BV/Second : "+str(round(self.bv/(self.record["gaming"][-1]["time"]/1000),5)),C.BLACK,(276,500),2,C.WHITE,True)
                         
    def get_record_info(self,record_info,record):
        self.record_info = record_info
        for i in record:
            if i[0] == record_info:
                self.record = i[1]
                break
        self.bv = self.count_3bv(self.record["mines_map"])
        
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

    def blit_title2(self,screen,font,text,color,cordinate,frame,frame_color,center=False):
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]+frame,cordinate[1]+frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]-frame,cordinate[1]-frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]+frame,cordinate[1]-frame),center)
        tool.blit_text(screen,font,text,frame_color,(cordinate[0]-frame,cordinate[1]+frame),center)
        tool.blit_text(screen,font,text,color,cordinate,center)

    def count_3bv(self,map):
        count = 0
        global visited
        global container
        container = []
        visited = [[False for _ in range(len(map[0]))] for _ in range(len(map))]
        for i in range(len(map)):
            for j in range(len(map[i])):
                if visited[i][j] == False and map[i][j] == 0:
                    count += 1
                    container.append((i,j))
                    while len(container) != 0:
                        self.flood_fill_mark(map,container[0][0],container[0][1])
                        container.pop(0)
        
        for i in range(len(map)):
            for j in range(len(map[i])):
                if visited[i][j] == False and map[i][j] != 10:
                    count += 1
                    visited[i][j] = True
            #         print("#",end="")
            #     elif visited[i][j]==False:
            #         print(".",end="")
            #     elif visited[i][j]==True:
            #         print("*",end="")
            # print()
        return count

    def flood_fill_mark(self,map, i, j):
        if i < 0 or i >= len(map) or j < 0 or j >= len(map[i]):
            return
        if visited[i][j] ==  True:
            return
        visited[i][j] = True
        if map[i][j] == 0:
            container.append((i-1,j))
            container.append((i+1,j))
            container.append((i,j-1))
            container.append((i,j+1))
            container.append((i-1,j-1))
            container.append((i-1,j+1))
            container.append((i+1,j-1))
            container.append((i+1,j+1))